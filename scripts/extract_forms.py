#!/usr/bin/env python

import requests
import re
from bs4 import BeautifulSoup
import urllib.parse



def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError: 
        pass


target_url = "https://facebook.com"
response = request(target_url)

parsed_html = BeautifulSoup(response.content,features="lxml")
forms_list = parsed_html.findAll("form")

#print(forms_list)
for form in forms_list:
    action = form.get("action")
    post_url = urllib.parse.urljoin(target_url, action)
    print(action)
    method = form.get("method")
    print(method)

    inputs_list = form.findAll("input")
    post_data = {}
    for input_elem in inputs_list:
        input_name = input_elem.get("name")
        input_value = input_elem.get("value")
        input_type = input_elem.get("type")
        if input_type == 'text':
            input_value = "test"
        post_data[input_name] = input_value
        print (input_name)
    result = requests.post(post_url,data=post_data)
    print(response.content)
