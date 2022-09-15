from cmath import log10
import jenkins
import paramiko
import re
from collections import defaultdict
from timeline.models import *
import os

class datafetch:
    def __init__(self, username: str, password: str, url: str) -> None:
        self.username = username
        self.password = password
        self.url = url
    def setup_connection(self) -> jenkins:
        jenkins_client = jenkins.Jenkins(self.url, username = self.username, password = self.password)
        return jenkins_client
    def get_all_views(self, connection: jenkins) -> list:
        return connection.get_views()
    def get_all_jobs(self, connection: jenkins) -> list:
        return connection.get_all_jobs()
    def get_all_nodes(self, connection: jenkins) -> list:
        return connection.get_nodes()

# creates a dictionary with ip address as keys, data as values
def log_prep(line, k, temp_ip, temp_id, log_id):
    line = line.strip()
    line = str(line).split(' ')
    log1 = Log()
    log2 = Log()
    tm = Timeline()
    rq = Request()
    data = Data()
    log_ID = str(log_id)
    ID = temp_id
    if not k % 2:
        ip = re.sub("http://", "", line[10], 1)
        ip = re.sub("[A-Za-z/]", "", ip)

        tm.IP = ip
        tm.save()

        # request log
        datetime = line[0] + ' ' + line[1]
        type = 'SENT'
        restLogger = line[6]
        hostname = line[3]

        log1.ID = log_ID
        log1.dateTime = datetime
        log1.type = type
        log1.restLogger = restLogger
        log1.hostname = hostname
        log1.timeline = tm

        log1.save()

        # request object
        requestType = 'POST'
        params = line[8]
        URL = line[10:]
        URL = " ".join(URL)

        rq.ID = ID
        rq.requestType = requestType
        rq.params = params
        rq.URL = URL
        rq.log = log1

        rq.save()

        return ip
    else:
        tm.IP = temp_ip
        tm.save()
       
        return_code = re.sub("[^0-9]", "", line[8])
        result = line[13].replace(',', '')
        slave = re.sub('[",]', '', line[9])
        role = re.sub('["}]', '', line[15])

        #received log
        datetime = line[0] + ' ' + line[1]
        type = 'RECEIVED'
        restlogger = line[6]
        master = line[3]
        ip = re.sub('[",]', '', line[11])

        log2.ID = log_ID
        log2.dateTime = datetime
        log2.type = type
        log2.restLogger = restlogger
        log2.hostname = master
        log2.timeline = tm

        log2.save()

        # default data object
        data.ID = ID
        data.statusCode = return_code
        data.hostname = slave
        data.ip = ip
        data.result = result
        data.role = role
        data.log = log2

        data.save()

def file_prep(line, temp_ip, temp_id, log_id):
    if 'SENT:' in line:
        #LOG
        datetime = line[0] + ' ' + line[1][0:12]
        hostname = line[3]
        type = ''
        restlogger = line[line.index('vRestLogger:') + 1]
        if 'CONF' in line[line.index(restlogger) + 1]:
            type = line[line.index(restlogger) + 1] + ' ' + line[line.index(restlogger) + 2]
        else:
            type = line[line.index(restlogger) + 1]

        #REQUEST
        requestType = line[line.index('-X') + 1]
        params = '-X'
        URL = line[(line.index('-X') + 2):]
        URL = " ".join(URL)

        #TIMELINE
        ip = line[line.index(requestType) + 1]
        ip = re.sub("http://", "", ip, 1)
        ip = re.sub("[A-Za-z/]", "", ip)
        #print(line)
        print('LOG:')
        print('datetime =', datetime, 'hostname =', hostname, 'type =', type, 'restlogger =', restlogger, 'ID =', log_id)
        print('REQUEST:')
        print('requestType =', requestType, 'params =', params, 'URL =', URL, 'ID =', temp_id)
        return ip
    else:
        #LOG
        datetime = line[0] + ' ' + line[1][0:12]
        hostname = line[3]
        type = ''
        restlogger = line[line.index('vRestLogger:') + 1]
        if 'CONF' in line[line.index(restlogger) + 1]:
            type = line[line.index(restlogger) + 1] + ' ' + line[line.index(restlogger) + 2]
        else:
            type = line[line.index(restlogger) + 1]

        #RESPONSE
        return_code = line[line.index('RECEIVED:') + 1][0:3]
        hostname = 'Slave_1'
        result = line[line.index('RECEIVED:') + 1][4:]
        ip = temp_ip
        role = 'SLAVE'
        res = line[line.index('RECEIVED:') + 1]
        index = res.find('"result')
        result = res[index:]

        #print(line)
        print('LOG:')
        print('datetime =', datetime, 'hostname =', hostname, 'type =', type, 'restlogger =', restlogger, 'ID =', log_id)
        print('RESPONSE')
        print('return code =', return_code, 'hostname =', hostname, 'result =', result, 'ip =', ip, 'role =', role, 'ID =', temp_id)



# sets up connection with jenkins server, uses log_prep() function to create and return a dictionary
# with processed log data
def log_process():
    host = "10.14.222.120"
    port = 50022
    username = "student"
    password = "student!"

    BuildNum = 0

    fetch = datafetch(username, password, 'http://10.14.222.120:50088//')
    jenkins_client = fetch.setup_connection()

    next_bn = jenkins_client.get_job_info('math_test')['nextBuildNumber']
    
    for i in range(1,next_bn):
        try:
            res = jenkins_client.get_build_info('math_test', i)['result']
        except:
            continue
        if "SUCCESS" in res:
            BuildNum = i

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    stdin, stdout, stderr = ssh.exec_command("cd jenkins_home/jobs/math_test/builds/" + str(BuildNum) + "/archive; cat RESTlog.log")
    lines = stdout.readlines()
    ssh.close()

    temp_ip = 0
    temp_id = 1
    log_id = 1
    for k, line, in enumerate(lines):
        temp_ip = log_prep(line, k, temp_ip, temp_id, log_id)
        if k % 2 != 0:
            temp_id += 1
        log_id += 1

def file_process(name):
    file = open(name, 'r')
    lines = file.readlines()

    temp_ip = 0
    temp_id = 1
    log_id = 1
    data = Timeline.objects.all()
    data.delete()
    for k, line, in enumerate(lines):
        temp_ip = log_prep(line, k, temp_ip, temp_id, log_id)
        if k % 2 != 0:
            temp_id += 1
        log_id += 1

def file_process_better():
    sent_len = []
    rec_len = []
    temp_ip = 0
    temp_id = 1
    log_id = 1
    with open('vrest.log', encoding='utf-8') as file:
    #file = open('vrest.log', 'r').readlines()[1::2]
        for k, line in enumerate(file):
            if k == 100:
                break
            line = line.strip()
            line = str(line).split(' ')
            line = [i for i in line if i]
            if 'SENT:' in line or 'RECEIVED:' in line:
                temp_ip = file_prep(line, temp_ip, temp_id, log_id, sent_len, rec_len)
                log_id += 1
                if log_id % 2 != 0:
                    temp_id += 1


