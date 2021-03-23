#!/usr/bin/python

import sys
import os
import subprocess
from urllib.parse import urlparse

if len(sys.argv) != 3:
    print ("Usage: scan.py <target url> <scan name>")
    sys.exit(0)


url = str(sys.argv[1])
name = str(sys.argv[2])
#folders = ["/usr/share/dirb/wordlists", "/usr/share/dirb/wordlists/vulns"]
hosts = []

def nmap_scan():
    try:
        print ("INFO: Performing nmap scan for " + url)
        hostname = urlparse(url).hostname # prints www.website.com
        print (hostname)
        HOSTCMD = "host %s | grep 'has address' | cut -d' ' -f4" % (hostname)
        results = subprocess.check_output(HOSTCMD, shell=True)
        results = results.decode()
        print (results)
        #lines = results.split("\n")
        lines = results.splitlines()
        for line in lines:
            print ("line: " + line.strip())
            hosts.append(line.strip())
        for hname in hosts:    
            print ("INFO: Performing nmap scan for " + hname)    
            NMAPSCAN = "nmap -sT -Pn -vv -T4 -p- -oN %s_allports.nmap  %s" % (hname, hname)
            results = subprocess.check_output(NMAPSCAN, shell=True)
    except:
            pass


def dirb_scan():
    found = []
    print ("INFO: Starting dirb scan for " + url)
    #for folder in folders:
    #    for filename in os.listdir(folder):
    filename = "/usr/share/dirb/wordlists/common.txt"
    if not os.path.exists(os.path.join(os.getcwd(), 'results')):
        os.mkdir(os.path.join(os.getcwd(),'results'));

    outfile = " -o " + "results/" + name + "_dirb_common.txt"
    DIRBSCAN = "dirb %s %s %s -S -r" % (url, filename, outfile)
    try:
        print (DIRBSCAN)
        results = subprocess.check_output(DIRBSCAN, shell=True)
        resultarr = results.split("\n")
        for line in resultarr:
            if "+" in line:
    	        if line not in found:
    	            found.append(line)
    except:
        pass
    
    try:
        if found[0] != "":
            print ("[*] Dirb found the following items...")
            for item in found:
                print ("   " + item)
    except:
        print ("INFO: No items found during dirb scan of " + url)		


def nikto_scan():
    found=[]
    if not os.path.exists(os.path.join(os.getcwd(), 'results')):
        os.mkdir(os.path.join(os.getcwd(),'results'));
    outfile = " -o " + "results/" + name + "_nikto.txt" 
    NIKTOSCAN = "nikto -h %s  %s " % (url, outfile)
    try:
        print (NIKTOSCAN)
        results = subprocess.check_output(NIKTOSCAN, shell=True)
        resultarr = results.split("\n")
        for line in resultarr:
            if "+" in line:
    	        if line not in found:
    	            found.append(line)
    except:
        pass
    
    try:
        if found[0] != "":
            print ("[*] Nikto found the following items...")
            for item in found:
                print ("   " + item)
    except:
        print ("INFO: No items found during nikto scan of " + url)		

def ssl_scan():
    try:
        SSLSCAN = "/home/kali/repos/testssl.sh/testssl.sh -oA sslscan-output %s" %(url)
        results = subprocess.check_output(SSLSCAN, shell=True)
    except:
        pass


ssl_scan()
dirb_scan()
nikto_scan()
nmap_scan()
