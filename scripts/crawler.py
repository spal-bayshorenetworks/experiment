#!/usr/bin/env python

import requests
import re
import urllib.parse as urlparse


'''
def request(url):
    try:
        return requests.get("https://" + url)
    except requests.exceptions.ConnectionError: 
        pass


target_url = "google.com"

with open("subdomains.list","r") as wordlist_file:
    for line in wordlist_file:
        test_url = line.strip() + "." + target_url
        response = request(test_url)
        print(test_url)
        if response:
            print("[+] Discovered Subdomain ---> " + test_url)

'''


target_url = "https://zsecurity.org"
target_links = []

def extract_links_from(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"',response.content.decode(errors="ignore"))

def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        link = urlparse.urljoin(url,link)
    
        if '#' in link:
            link = link.split('#')[0]
    
        if target_url in link and link not in target_links:
            target_links.append(link)
            print (link)
            crawl(link)
            

crawl(target_url)