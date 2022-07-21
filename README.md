# lcpy

## 描述

lcpy是lcx用python的实现。是一款端口转发工具，用于内网渗透场景。主要功能有将本地端口转发到远程主机某个端口上，将本地端口转发到本地另一个端口上，以及进行监听并进行转发使用。

## 编译

除了使用python3环境运行该工具，也可在Windows和Linux环境下编译生成二进制文件。

pip install pyinstaller
pyinstaller -F lcpy.py

## 用法

usage: lcx_py_v0.2 [-h] [-m] [-p1] [-p2] [-p] [-SP] [-RP]

```
optional arguments:
  -h, --help            show this help message and exit
  -m , --listen_method 
                        The default listening address
  -p1 , --listen_port1 
                        The listening port1
  -p2 , --listen_port2 
                        The listening port2
  -p , --listen_port    The listening port
  -SP , --targetAddressPort 
                        The targetIP:Port
  -RP , --remoteAddressPort 
                        The RemoteIP:Port
```

## 示例

监听模式
-m listen -p1 9001 -p2 9002

tran模式
./lcpy -m tran -p 8001 -RP 10.8.58.239:22

slave模式
-m slave -SP 10.8.58.239:22 -RP 10.8.58.243:9001

