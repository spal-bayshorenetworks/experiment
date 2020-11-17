#!/usr/bin/env python

import requests

def download(url):
    get_response = requests.get(url)
    print(get_response.content)
    file_name = url.split('/')[-1]
    with open(file_name,"wb") as out_file:
        out_file.write(get_response.content)


download("https://images.nvidia.com/geforce/sites/default/files-world/geforce-gtx-760-style1.png")

