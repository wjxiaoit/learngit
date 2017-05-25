Git is a distributed version control system.
Git is free software distributed under the GPL.
Git has a mutable index called stage.
Git tracks changes of files.
My stupid boss still prefers SVN.

2017-05-25
添加python 获取IP的脚本，get_ip.py
1、通过socket直接获取外网IP
2、获取指定网卡的IP

添加检测游戏服是否正常的脚本，发现问题可以通过微信通知，并且进行重启；check_port_process.py
1、检测端口是否处理监听
2、检查进程数是否为3个
3、发现异常，通过微信通知
4、发现异常，通知后重启，并再次检测
