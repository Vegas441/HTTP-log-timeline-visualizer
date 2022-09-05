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



# sets up connection with jenkins server, uses log_prep() function to create and return a dictionary
# with processed log data
def log_process():
    host = "10.14.222.120"
    port = 50022
    username = "student"
    password = "student!"

    BuildNum = 20

    fetch = datafetch(username, password, 'http://10.14.222.120:50088//')
    jenkins_client = fetch.setup_connection()

    next_bn = jenkins_client.get_job_info('math_test')['nextBuildNumber']
    result = jenkins_client.get_build_info('math_test', BuildNum)['result']

    if "SUCCESS" not in result:
        print('this build failed, exiting')
        exit(1)

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
