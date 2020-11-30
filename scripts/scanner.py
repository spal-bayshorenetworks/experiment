#!/usr/bin/env python

import requests
import re
import urllib.parse
from bs4 import BeautifulSoup

class Scanner:
    def __init__(self, url, ignore_links):
        self.target_url = url
        self.session = requests.Session()
        self.target_links = []
        self.links_to_ignore = ignore_links

    def extract_links_from(self, url):
        response = self.session.get(url)
        return re.findall('(?:href=")(.*?)"',response.content.decode(errors="ignore"))

    def crawl(self, url=None):
        if url == None:
            url = self.target_url
        href_links = self.extract_links_from(url)
        for link in href_links:
            link = urllib.parse.urljoin(url,link)
        
            if '#' in link:
                link = link.split('#')[0]
        
            if self.target_url in link and link not in self.target_links and link not in self.links_to_ignore:
                self.target_links.append(link)
                print (link)
                self.crawl(link)


    def extract_forms(self, url):
        response = self.session.get(url)
        parsed_html = BeautifulSoup(response.content,features="lxml")
        return parsed_html.findAll("form")

    def submit_form(self, form, value, url):
        action = form.get("action")
        post_url = urllib.parse.urljoin(url, action)
        #print(action)
        method = form.get("method")
        #print(method)
    
        inputs_list = form.findAll("input")
        post_data = {}
        for input_elem in inputs_list:
            input_name = input_elem.get("name")
            input_value = input_elem.get("value")
            input_type = input_elem.get("type")
            if input_type == 'text':
                input_value = value
            post_data[input_name] = input_value
            #print (input_name)
        if method == 'post':
            return self.session.post(post_url, data=post_data)
        return self.session.get(post_url,params=post_data)

    def run_scanner(self):
        for link in self.target_links:
            forms = self.extract_forms(link)
            for form in forms:
                print("[+] Testing form in " + link)

            if "=" in link:
                print("[+] Testing link " + link)


