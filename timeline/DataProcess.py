import jenkins
import paramiko
import re
from collections import defaultdict

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
def log_prep(line, k, info, temp_ip):
    line = line.strip()
    line = str(line).split(' ')
    if not k % 2:
        #ip = re.sub("[^0-9\.]", "", line[-1])
        #ip = re.sub(":", "", ip, 1)
        #rychlejší verze, ale idk
        ip = re.sub("http://", "", line[-1], 1)
        ip = re.sub("[A-Za-z/]", "", ip)
        if ip not in info:
            info[ip] = []
        return ip
    else:
        new_list = []
        time = line[1]
        new_list.append(time)
        type_received = re.sub(":", "", line[7])
        new_list.append(type_received)
        rest_logger = line[6]
        new_list.append(rest_logger)
        master = line[2] + ' ' + line[3] + ' ' + line[4]
        new_list.append(master)
        return_code = re.sub("[^0-9]", "", line[8])
        new_list.append(return_code)
        new_list.append(temp_ip)
        result = line[13].replace(',', '')
        new_list.append(result)
        slave = re.sub('[",]', '', line[9])
        new_list.append(slave)
        role = re.sub('["}]', '', line[15])
        new_list.append(role)
        # slave = line[9].replace('"', '')
        # slave = slave.replace(',', '')
        info[temp_ip].append(new_list)

# sets up connection with jenkins server, uses log_prep() function to create and return a dictionary
# with processed log data
def log_process():
    host = "10.14.222.120"
    port = 50022
    username = "student"
    password = "student!"

    BuildNum = 21

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

    info = defaultdict(dict)
    temp_ip = 0
    for k, line, in enumerate(lines):
        temp_ip = log_prep(line, k, info, temp_ip)
    return info
