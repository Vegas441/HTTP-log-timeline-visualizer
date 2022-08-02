import paramiko
import subprocess
import jenkinsapi
from jenkinsapi import jenkins
#from jenkinsapi.jenkins import Jenkins

#subprocess.run('ssh student@10.14.222.120 -p 50022', shell=True)

#proc = subprocess.Popen(['ssh', 'student@10.14.222.120 -p 50022'], stdin=subprocess.PIPE)
#proc.stdin.write('student!')

# proc = subprocess.Popen('ssh student@10.14.222.120 -p 50022', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

host = "10.14.222.120"
port = 50022
username = "student"
password = "student!"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, username, password)

_, NextBuild, _ = ssh.exec_command("cd jenkins_home/jobs/math_test; cat nextBuildNumber")

build_num = NextBuild.readlines()
print('Enter desired test number: ')
Desired_num = input()
if int(Desired_num) >= int(build_num[0]):
    print('This test does not exist')
    exit(1)

stdin, stdout, stderr = ssh.exec_command("cd jenkins_home/jobs/math_test/builds/" + Desired_num + "; cat log")
lines = stdout.readlines()
if "SUCCESS" not in lines[-1]:
    print('no log, test failed')
    exit(1)
stdin, stdout, stderr = ssh.exec_command("cd jenkins_home/jobs/math_test/builds/" + Desired_num + "/archive; cat RESTlog.log")
lines = stdout.readlines()
print(lines)
ssh.close()

# class datafetch:
#     def __init__(self, username: str, password: str, url: str) -> None:
#         self.username = username
#         self.password = password
#         self.url = url
#     def setup_connection(self) -> jenkins:
#         jenkins_client = jenkins.Jenkins(self.url, username = self.username, password = self.password)
#         return jenkins_client
#     def get_all_views(self, connection: jenkins) -> list:
#         return connection.get_views()
#     def get_all_jobs(self, connection: jenkins) -> list:
#         return connection.get_all_jobs()
    
# fetch = datafetch('student', 'student!', 'http://10.14.222.120:50088//')
# jenkins_client = fetch.setup_connection()
# print(fetch.get_all_views(jenkins_client))
# print(fetch.get_all_jobs(jenkins_client))

# def get_server_instance():
#     jenkins_url = 'http://10.14.222.120:50088//'
#     server = Jenkins(jenkins_url, username = 'student', password = 'student!')
#     return server

# server = get_server_instance()
# jobs = server.get_jobs()
# print(jobs)
# last_build_number = server.get_job_info('math_test')['lastCompletedBuild']['number']
# print(last_build_number) # prints XML configuration

