#!/use/bin/env python

import scapy.all as scapy
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target",help="Please enter the target ip address or ip range")
    (options,arguments) = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify target ip address or ip range. Use --help for more info")
    return options

def scan(ip):
    # scapy.arping(ip)
    arp_request = scapy.ARP(pdst=ip)
    # print(arp_request.summary())
    # arp_request.show()
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    # print(broadcast.summary())
    # broadcast.show()
    broadcast_arp_request = broadcast/arp_request
    # broadcast_arp_request.show()
    # print(scapy.ls(scapy.ARP()))
    # print(scapy.ls(scapy.Ether()))
    # answered_list, unanswered_list = scapy.srp(broadcast_arp_request, timeout=1)
    # print(answered_list.summary())
    # print(unanswered_list.summary())
    answered_list = scapy.srp(broadcast_arp_request, timeout=1,verbose=False)[0]
    # print("IP\t\t\tMAC Address\n--------------------------------------------------")
    clients_list = []
    for element in answered_list:
        # print(element)
        client_dict = {"ip":element[1].psrc,"mac":element[1].hwsrc}
        clients_list.append(client_dict)
        # print(element[1].psrc + "\t\t" + element[1].hwsrc)
    return clients_list

def print_result(clients):
    print("IP\t\t\tMAC Address\n--------------------------------------------------")
    for client in clients:
        print(client["ip"] + "\t\t" + client["mac"])

options = get_arguments()
clients_list = scan(options.target)
print_result(clients_list)
