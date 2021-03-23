#!/usr/bin/python3

import requests
from string import ascii_lowercase

#r = requests.get("https://www.gsa.gov")
#print (r.text)
#print (r.headers['server'])
url = "https://www.gsa.gov/"

for char1 in ascii_lowercase:
    for char2 in ascii_lowercase:
        for char3 in ascii_lowercase:
            directory = char1+char2+char3
            r = requests.get(url+directory)
            if r.status_code != 404:
                print (url+directory+" : "+str(r.status_code))
