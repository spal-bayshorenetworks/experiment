import logging
import os
import fnmatch
import re
import inspect
import struct
import socket
import binascii
import time
import random

# First six bytes are null and not included in payloads below (Leading 3 H's in struct.pack fmt)
payloads = [[0, 0, 8, 5, 23, 2, 5, 0, 0, 0, 150],                # Doesn't trigger policy 1
           [0, 0, 12, 5, 23, 2, 5, 0, 0, 0, 0, 0, 0, 0, 150],   #   "        "       "2
           [0, 0, 8, 5, 15, 0, 0, 0, 0, 0, 150],                #   "        "       "3
           [0, 0, 8, 5, 1, 0, 0, 0, 0, 0, 150],                 #   "        "       "4
           [0, 0, 8, 5, 16, 0, 0, 0, 0, 0, 150],                #   "        "       "5
           [0, 0, 8, 5, 2, 0, 0, 0, 0, 0, 150],                 #   "        "       "6
           [0, 0, 8, 5, 4, 0, 0, 0, 0, 0, 150],                 #   "        "       "7
           [0, 0, 8, 5, 3, 0, 0, 0, 0, 0, 150],                 #   "        "       "8
           [0, 0, 8, 5, 23, 2, 5, 40, 0, 0, 150],               # triggers bc352c3eb4c111e585d0080027b3fa86 offset 10  "9
           [0, 0, 12, 5, 23, 2, 5, 0, 0, 0, 0, 50, 0, 0, 150],  #   "      3cfc6dbab4c111e585d0080027b3fa86 offset 14  "10
           [0, 0, 8, 5, 15, 0, 0, 30, 0, 0, 150],               #   "      d5bbc2f8b4bc11e585d0080027b3fa86 offset 10  "11
           [0, 0, 8, 5, 1, 0, 0, 30, 0, 0, 150],                #   "      dd60f37cb4bf11e585d0080027b3fa86 offset 10  "12
           [0, 0, 8, 5, 16, 0, 0, 30, 0, 0, 150],               #   "      5a6e0a1cb4c011e585d0080027b3fa86 offset 10  "13
           [0, 0, 8, 5, 2, 0, 0, 9, 0, 0, 150],                 #   "      0ac4f460b4c211e585d0080027b3fa86 offset 10  "14
           [0, 0, 8, 5, 4, 0, 0, 2, 0, 0, 150],                 #   "      9b14f560b4c211e585d0080027b3fa86 offset 10  "15
           [0, 0, 8, 5, 3, 0, 0, 1, 0, 0, 150],                #   "      d14a6e3ab4c211e585d0080027b3fa86 offset 10  "16
           [0, 0, 11, 5, 16, 0, 2, 0, 2, 4, 255, 254, 255, 254], #17
           [0, 0, 14, 5, 21, 8, 6, 0, 1, 0, 0, 0, 2, 0, 3, 0, 3], #18
           [0, 0, 14, 5, 21, 9, 6, 0, 1, 0, 0, 0, 2, 0, 3, 0, 3], #19
           [0, 0, 16, 5, 21, 13, 6, 0, 4, 0, 7, 0, 3, 6, 175, 4, 190, 16, 13], #20
           [0, 0, 16, 5, 21, 252, 5, 0, 4, 0, 7, 0, 3, 6, 175, 4, 190, 16, 13], #21
           [0, 0, 16, 5, 21, 13, 5, 0, 4, 0, 7, 0, 3, 6, 175, 4, 190, 16, 13], #22
           [0, 0, 6, 5, 8, 0, 1, 254, 0], #23
           [0, 0, 6, 5, 8, 0, 4, 0, 0], #24
           [0, 0, 2, 5, 7], #25
           [0, 0, 2, 5, 11], #26
           [0, 0, 2, 5, 12], #27
           [0, 0, 2, 5, 17], #28
           [0, 0, 10, 5, 20, 7, 6, 0, 1, 0, 2, 0,5], #29
           [0, 0, 4, 5, 24, 0, 0], #30
           [0, 0, 5, 5, 43, 14, 1, 0], #31
           [0, 0, 5, 5, 43, 13, 1, 0], #32
           [0, 0, 6, 5, 5, 0, 1, 0, 0], #33
           [0, 0, 6, 5, 6, 0, 1, 1, 1], #34
           [0, 0, 8, 5, 22, 0, 4, 0, 242, 0, 37], #35
           [0, 0, 11, 5, 16, 0, 2, 65, 2, 4, 64, 64, 64, 64], #36
           [0, 0, 11, 5, 16, 0, 2, 245, 2, 4, 64, 64, 64, 64], #37
           [0, 0, 15, 5, 23, 0, 0, 0, 16, 0, 0, 0, 2, 4, 0, 0, 0, 0],  #38
           [0, 0, 15, 5, 23, 0, 0, 0, 06, 0, 0, 0, 2, 4, 0, 0, 0, 0],  #39
           [0, 0, 15, 5, 23, 0, 9, 0, 06, 0, 9, 0, 2, 4, 0, 3, 0, 9],  #40
           [0, 0, 15, 5, 23, 0, 9, 0, 06, 0, 0, 0, 2, 4, 0, 3, 0, 9],  #41
           ] 



def do_cont():
    while True:
        try:
            z = random.choice(payloads)
    
            s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
            #s.setblocking(1)
            s.settimeout(15.0)
            s.connect ( ("192.168.100.151", 502) )
            #s.connect ( ("127.0.0.1", 5502) )
            bytelen = len(z)-3
            bytelen =  "B"*bytelen
            v = struct.pack ( ">HHH%s"%bytelen, *z) 
            print " [*] Sending payload: %s, %s" % (binascii.hexlify(v),z)
            
            s.send (v)
            r = s.recv (1000)
    
            print r
         
            print "RES: %s" %binascii.hexlify(r)
            s.close()
    
        except Exception as e:
           # print "ERR: %s" % str(e)
            pass

# Enable below to slow down traffic
#    time.sleep(random.randint(1/2,1))

def send_modbus_payload(idx):
    s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    #s.setblocking(1)
    s.settimeout(15.0)
    try:
        #s.connect ((envvars.getModbusListenerIp(), envvars.modbus_port))
        #s.connect ( ("192.168.100.127", 502) )
        #s.connect ( ("192.168.100.151", 502) )
        s.connect ( ("192.168.100.70", 502) )
        # for i in payloads:
        i = payloads [idx]
        bytelen = len(i)-3
        bytelen =  "B"*bytelen
        v = struct.pack ( ">HHH%s"%bytelen, *i) 
        print i, "REQ: %s" % binascii.hexlify(v)
            
        s.send (v)
        r = s.recv (1000)
            
        # print "RESPONSE LENGTH: %s" %len(r)
        print "RES: %s" %binascii.hexlify(r)
            
        s.close()
    except Exception as e:
        print "ERR: %s" % str(e)
        s.close()
        pass


send_modbus_payload (3)
#send_modbus_payload (9)
#send_modbus_payload (33)
#send_modbus_payload (40)
#send_modbus_payload (37)
#send_modbus_payload (40)
#send_modbus_payload (27)
#send_modbus_payload (35)
#send_modbus_payload (36)
#do_cont()
