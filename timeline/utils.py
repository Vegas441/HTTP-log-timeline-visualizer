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

def file_prep(line, temp_ip, temp_id, log_id):
    log = Log()
    tm = Timeline()
    rq = Request()
    data = Data()
    log_ID = str(log_id)
    rq_id = temp_id
    data_id = temp_id

    try:
        log_ID = (Log.objects.last().ID) + 1
        print(Log.objects.last().type)
        print(Log.objects.last().dateTime)
        rq_id = (Request.objects.last().ID) + 1
        data_id = (Data.objects.last().ID) + 1
    except Exception:
        pass

    #LOG
    datetime = line[0] + ' ' + line[1]
    hostname = line[3]
    type = ''
    try:
        restlogger = line[line.index('vRestLogger:') + 1]
    except:
        restlogger = line[line.index('RestLogger:') + 1]
    if 'CONF' in line[line.index(restlogger) + 1]:
        type = line[line.index(restlogger) + 1] + ' ' + line[line.index(restlogger) + 2]
    else:
        type = line[line.index(restlogger) + 1]
    type = re.sub(":", "", type)

    
    if 'SENT:' in line:
        #REQUEST
        requestType = line[line.index('-X') + 1]
        params = '-X'
        URL = line[(line.index('-X') + 2):]
        URL = " ".join(URL)


        #TIMELINE
        ip = line[line.index(requestType) + 1]
        sub_ip = ip.split('/')
        ip = sub_ip[2]

        tm.IP = ip
        tm.save()

        log.ID = log_ID
        log.dateTime = datetime
        log.type = type
        log.restLogger = restlogger
        log.hostname = hostname
        log.timeline = tm

        log.save()

        rq.ID = rq_id
        rq.requestType = requestType
        rq.params = params
        rq.URL = URL
        rq.log = log

        rq.save()

        print(tm.IP)
        print(rq.ID, rq.requestType, rq.params, rq.URL, rq.log.dateTime, rq.log.ID)
        print(log.ID, log.dateTime, log.type, log.restLogger, log.hostname)
        return ip
    else:
        #RESPONSE
        return_code = line[line.index('RECEIVED:') + 1][0:3]
        result = '  '.join(line[(line.index('RECEIVED:') + 1):])
        result = result[4:]
        ip = temp_ip

        tm.IP = temp_ip
        tm.save()

        log.ID = log_ID
        log.dateTime = datetime
        log.type = type
        log.restLogger = restlogger
        log.hostname = hostname
        log.timeline = tm

        log.save()

        data.ID = data_id
        data.statusCode = return_code
        data.ip = ip
        data.data = result
        data.log = log

        data.save()

        print(tm.IP)
        print(data.ID, data.statusCode, data.ip, data.data, data.log.dateTime, data.log.ID)
        print(log.ID, log.dateTime, log.type, log.restLogger, log.hostname)

        return ip



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

    BuildNum = 21

    stdin, stdout, stderr = ssh.exec_command("cd jenkins_home/jobs/math_test/builds/" + str(BuildNum) + "/archive; cat RESTlog.log")
    lines = stdout.readlines()
    ssh.close()

    temp_ip = 0
    temp_id = 1
    log_id = 1
    data = Timeline.objects.all()
    data.delete()
    for line in lines:
        line = line.strip()
        line = str(line).split(' ')
        line = [i for i in line if i]
        if 'SENT:' in line or 'RECEIVED:' in line:
            temp_ip = file_prep(line, temp_ip, temp_id, log_id)

def file_process(name):
    temp_ip = 0
    temp_id = 1
    log_id = 1
    data = Timeline.objects.all()
    data.delete()
    with open(name, encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            line = str(line).split(' ')
            line = [i for i in line if i]
            if 'SENT:' in line or 'RECEIVED:' in line:
                temp_ip = file_prep(line, temp_ip, temp_id, log_id)
