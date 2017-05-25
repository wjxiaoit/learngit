#!/bin/env python
#coding: utf-8
import socket
import re
import os


def valid_ip(ip):
    if ('255' in ip) or (ip == "0.0.0.0"):
        return False
    else:
        return True

def get_wan_ip_addr():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        return s.getsockname()[0]

def get_ip_addr(ifname):
	shell_str="LANG=c ifconfig %s" %(ifname)
        if_data = ''.join(os.popen(shell_str).readlines())
        ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',if_data, flags=re.M)
        ip = filter(valid_ip,ips)
        return ip[0]

if __name__=='__main__':
    ip1=get_ip_addr('enp0s8')
    ip2=get_wan_ip_addr()
    print "%s %s" %(ip1,ip2)
