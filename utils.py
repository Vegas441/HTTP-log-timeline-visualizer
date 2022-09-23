import jenkins
import re
from timeline.models import *
import requests

class datafetch:
    def __init__(self, username: str, password: str, url: str) -> None:
        self.username = username
        self.password = password
        self.url = url
    def setup_connection(self) -> jenkins:
        jenkins_client = jenkins.Jenkins(self.url, username = self.username, password = self.password)
        return jenkins_client

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

        return ip

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

def link_file_process(url):
    fetch = datafetch(url = url, username='', password='')
    jenkins_client = fetch.setup_connection()
    url = url + '/restlog'
    try:
        req = requests.Request(method='GET', url=url)
    except:
        exit(-1)
    response = jenkins_client.jenkins_open(req)
    f = open('media/newfile.txt', 'w')
    f.write(response)
    f.close()
    file_process('media/newfile.txt')
    