import jenkins
import paramiko
from datetime import datetime

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
    
host = "10.14.222.120"
port = 50022
username = "student"
password = "student!"
    
fetch = datafetch(username, password, 'http://10.14.222.120:50088//')
jenkins_client = fetch.setup_connection()

next_bn = jenkins_client.get_job_info('math_test')['nextBuildNumber']
result = jenkins_client.get_build_info('math_test', 20)['result']
time = int(jenkins_client.get_build_info('math_test', 20)['timestamp'])
time /= 1000
date = datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
if "SUCCESS" not in result:
    print('this build failed, exiting')
    exit(1)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, username, password)

stdin, stdout, stderr = ssh.exec_command("cd jenkins_home/jobs/math_test/builds/20/archive; cat RESTlog.log")
lines = stdout.readlines()
print(lines)
ssh.close()

print(date)