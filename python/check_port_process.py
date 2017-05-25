#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding:utf-8

"""
1、使用本脚本，需要先注册企业微信号；
2、注册后的替换本脚本的98，99行；
"""

import os
import requests
import json
import socket
import fcntl
import struct
import time

#设定不需要检测的区格式:1,2,4,5 默认为9999服,由于9999服不存在,所以默认全部检测
#No_check=5,6,7
No_check=9999

#定义游戏工程目录
Dir="/data/mob/mob_server/"

#获取在本机运行的游戏服号，排队不需要检测的服
def Get_game_dir(Dir):
    Game_dir=os.listdir(Dir)
    if 'nameserver' in Game_dir:
        Game_dir.remove('nameserver')
    Local_num=[int(i[3:]) for i in Game_dir]
    No_list=[i for i in No_check]
    Game_num=list(set(Local_num) - set(No_list))
    return Game_num

#查看对应游戏服的端口是否处于监听状态
def check_port(num):
    game_port=8000 + num
    shell_str1="netstat -anl|grep LISTEN |grep -w %d |wc -l"%(game_port)
    port_num=os.popen(shell_str1)
    return int(port_num.read())

#查看游戏进程是存在
def check_proc(num):
    shell_str2="ps -ef |grep 'knet_.*%dr'|grep -v grep|wc -l" %(num)
    proc_num=os.popen(shell_str2)
    return int(proc_num.read())

#获取本机IP地址
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

#获取当前时间
def get_time():
    shell_str3="date '+%Y-%m-%d %H:%M:%S'"
    time=os.popen(shell_str3)
    return time.read()[:-1]

#定义失败时的消息
def message_fail(num):
    ip = get_ip_address('eth1')
    dt = get_time()
    f_mes='主题: bin%s 检测发现异常，需要重启! 状态：ERROR 主机地址：%s  时间: %s 进程数： %d' %(num,ip,dt,pr)
    return f_mes
#定义重启正常后的消息
def message_ok(num):
    ip = get_ip_address('eth1')
    dt = get_time()
    ok_mes='主题: bin%s 重启成功，恢复正常! 状态：OK 主机地址：%s  时间: %s 进程数： %d' %(num,ip,dt,pr)
    return ok_mes

#定义重启失败后的信息
def message_ma(num):
    ip = get_ip_address('eth1')
    dt = get_time()
    ma_mes='主题: bin%s 重启失败，需要手动重启，请看到的同学马上处理 ! 状态：ERROR  主机地址：%s 时间: %s 进程数： %d' %(num,ip,dt,pr)
    return ma_mes

#进行重启操作
def reboot(num):
    S_dir=Dir+"/bin%d"%(num)
    os.chdir(S_dir)
    shell_str4="sh stop.sh"
    shell_str5="sh run.sh"
    os.system(shell_str4)
    time.sleep(3)
    os.system(shell_str5)



#获取企业微信token
def get_token():
    url='https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    values = {'corpid' : 'xxxxxx',
            'corpsecret' : 'xxxxxxxxxxxx',}
    req = requests.post(url, params=values)
    data = json.loads(req.text)
    return data['access_token']

#发送企业微信信息
def send_msg(ms):
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+get_token()
    values = """{"touser" : "1" ,
      "toparty":"1",
      "msgtype":"text",
      "agentid":"1",
      "text":{
        "content": "%s"
      },
      "safe":"0"
      }""" %(ms)
    data = json.loads(values)
    req = requests.post(url, values)



if __name__ == '__main__':
    server_num=Get_game_dir(Dir)
    for num in server_num:
        po=check_port(num)
        pr=check_proc(num)
        if po != 1 or pr != 3:
            ms=message_fail(num)
            send_msg(ms)
            reboot(num)
            po=check_port(num)
            pr=check_proc(num)
            if po == 1 and pr == 3:
                ms=message_ok(num)
                send_msg(ms)
            else:
                ms=message_ma(num)
                send_msg(ms)
