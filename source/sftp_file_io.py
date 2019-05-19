import sys
import os
from subprocess import Popen, PIPE, STDOUT
from time import sleep
import time
import subprocess
from os import waitpid, execv, read, write


class SFTPFileIO:

    def __init__(self):
        self.host_info = None
        self.remote_command = None
        self.remote_path = None
        self.local_path = None
        self.remote_response = None

    def execute(self, command):
        if command is None:
            value_error = ValueError('Empty command.')
            return value_error

        tokens = command.split(' ')
        if len(tokens) == 3:
            self.host_info = tokens[0].strip()
            self.remote_path = tokens[1].strip()
            self.local_path = tokens[2].strip()
            self.read()
        else:
            self.host_info = tokens[0].strip()
            self.remote_command = tokens[1].strip()
            self.execute_command()

    def read(self):
        ssh_process = subprocess.Popen(['sftp', self.host_info], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, universal_newlines=True, bufsize=1024)

        ssh_process.stdin.write("cd {0} \n".format(self.remote_path))
        # ssh_process.stdin.write("ls -lrt \n")
        ssh_process.stdin.write("get {0} {1} \n".format(self.remote_path, self.local_path))
        ssh_process.stdin.write("bye \n")
        ssh_process.stdin.close()

    def execute_command(self):
        print("execute command")
        #ssh_process = subprocess.Popen(['ssh', self.host_info], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      # stderr=subprocess.PIPE, universal_newlines=True, bufsize=1024)
        #ssh_process.stdin.write("{0};".format(self.remote_command))
        sshProcess = subprocess.Popen(['ssh', 'rejeesh@192.168.72.132'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE, universal_newlines=True, bufsize=0)
        sshProcess.stdin.write('root' + '\r')
        sshProcess.stdin.write("date;")
        sshProcess.stdin.close()

        # print(sshProcess.stdout.readlines())

        for line in sshProcess.stdout:
            if line == "END\n":
                break

            if self.remote_response is None:
                self.remote_response = line
            else:
                self.remote_response += line

            print(line, end="")
