# -*- coding: utf-8 -*-
import logging
import argparse
import socket
import threading
import time
from socket import *
import re
import sys
import os
import signal

# Constants
TIMEOUT = 0.1
DATANULLFLAG = 0
SOURCE_HOST = '127.0.0.1'
# source_port = 5000

def port_to_port(port1,port2):
    while 1:
        source_ip = "0.0.0.0"
        listen1 = serv_sock(source_ip, port1)
        listen2 = serv_sock(source_ip, port2)
        port_to_portconn1, addrLocal1 = listen1.accept()
        port_to_portconn2, addrLocal1 = listen2.accept()

        while 1:
            try:
                threading.Thread(target=forward, args=(port_to_portconn2, port_to_portconn1)).start()
                threading.Thread(target=forward, args=(port_to_portconn1, port_to_portconn2)).start()
                time.sleep(TIMEOUT)
                if DATANULLFLAG == 1:
                    print("Client is down, please rerun the program!")
                    os.kill(os.getpid(), signal.SIGKILL)
                    # break
            except:
                print("Client is down")
                break
        port_to_portconn1.close()
        port_to_portconn2.close()

def host_to_host(host1,host2):
    targetArraylist = host1.split(':')
    targetPort = int(targetArraylist[1])
    targetAddress = targetArraylist[0]
    remoteArraylist = host2.split(':')
    remotePort = int(remoteArraylist[1])
    remoteAddress = remoteArraylist[0]
    while 1:
        try:
            connLocal1 = socket(AF_INET, SOCK_STREAM)
            connLocal1.connect((targetAddress, targetPort))
            connLocal2 = socket(AF_INET, SOCK_STREAM)
            connLocal2.connect((remoteAddress, remotePort))

            while 1:
                threading.Thread(target=forward, args=(connLocal2, connLocal1)).start()
                threading.Thread(target=forward, args=(connLocal1, connLocal2)).start()
                time.sleep(TIMEOUT)
                if DATANULLFLAG == 1:
                    print("Client is down, please rerun the program!")
                    os.kill(os.getpid(), signal.SIGKILL)
        except:
            print("Server is down!")
            # os.kill(os.getpid(), signal.SIGKILL)
            break

def port_to_host(port, remoteAddress):
    while 1:
        localServSock = serv_sock(SOURCE_HOST, source_port)
        connLocal, addrLocal = localServSock.accept()
        connClient = socket(AF_INET, SOCK_STREAM)
        connClient.connect((remoteAddress, port))

        while 1:
            try:
                threading.Thread(target=forward, args=(connLocal, connClient)).start()
                threading.Thread(target=forward, args=(connClient, connLocal)).start()
                time.sleep(TIMEOUT)
                if DATANULLFLAG == 1:
                    print("Tunnel is down, please rerun the program!")
                    os.kill(os.getpid(), signal.SIGKILL)
            except:
                print("Tunnel is down!")
                # break '''Reserved words'''
        localServSock.close()

def forward(sender, recver):
    global DATANULLFLAG
    while 1:
        flag = 1
        # while 1:
        try:
            if flag == 0:
                break
            flag -= 1
            data = sender.recv(2048)
            if data == b'':
                DATANULLFLAG = 1
                # break
        except:
            print("recv error")
            break

        try:
            recver.sendall(data)
        except:
            print("send error")
            break

def serv_sock(ip,port):
    servSock = socket(AF_INET, SOCK_STREAM)
    servSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    servSock.bind((ip,port))
    servSock.listen(5)
    return servSock

def check_port(port):
    if re.match(r"^([0-9]{1,5})$", port):
        if (0 < int(port) <= 65536):
            return True
        else:
            logging.warning("Incorrect port, out of range.\n")
            return False
    else:
        logging.warning("Incorrect port, it should look like 'ip:port'.\n")
        return False

def check_url(host):
    hostArray = host.split(':')
    if len(hostArray) != 2:
        logging.warning("Input error, it should look like 'ip:port'.\n")
        return False
    ip = hostArray[0]
    port = hostArray[1]
    if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip) :
        if check_port(str(port)):
            return True
        else:
            # logging.warning("Incorrect port, it should look like 'ip:port'.\n")
            return False
    else:
        logging.warning("Incorrect IP, it should look like 'ip:port'.\n")
        return False

if __name__ == '__main__':
    logging.info('main start')
    print("""
    *******************
    ***Name: lcpy
    ***Version: v1.0
    *******************
    """)
    parsers = argparse.ArgumentParser(description='LCPY Start!')
    parsers.add_argument("-m", "--listen_method", metavar="", help='''
    tran : listen on PORT1 and connect to HOST2:PORT2
    listen: listen on Port1 and Port2
    slave: connect to HOST1:PORT1 and HOST2:PORT2
    ''')
    parsers.add_argument("-p1", "--listen_port1", metavar="", help="The listening Port1", type=int, default="9001")
    parsers.add_argument("-p2", "--listen_port2", metavar="", help="The listening Port2", type=int, default="9002")
    parsers.add_argument("-p", "--listen_port", metavar="", help="Listening Port", type=int, default="8001")
    parsers.add_argument("-SP", "--targetAddressPort", metavar="", help="TargetIP:Port", default="22")
    parsers.add_argument("-RP", "--remoteAddressPort", metavar="", help="RemoteIP:Port", default="9003")
    args = parsers.parse_args()

    if (args.listen_method == 'listen'):
        port1 = args.listen_port1
        port2 = args.listen_port2
        print("Using the Listen module, port1:%s port2:%s\n" % (port1, port2))
        if check_port(str(port1)) and check_port(str(port2)):
            t = threading.Thread(target=port_to_port, args=(port1, port2))
            t.start()
        else:
            sys.exit()

    if (args.listen_method == 'tran'):
        port = args.listen_port
        remoteAddressPort = args.remoteAddressPort
        print("Using the Tran module, the targethost is:", remoteAddressPort)
        if check_url(remoteAddressPort) and check_port(str(port)):
            source_port = args.listen_port
            arraylist = remoteAddressPort.split(':')
            remotePort = int(arraylist[1])
            remoteAddress = arraylist[0]
            t = threading.Thread(target=port_to_host, args=(remotePort, remoteAddress))
            t.start()
        else:
            sys.exit()

    if (args.listen_method == 'slave'):
        targetAddressPort = args.targetAddressPort
        remoteAddressPort = args.remoteAddressPort
        print("Using the Slave module, the targethost is:", targetAddressPort)
        if check_url(remoteAddressPort) and check_url(targetAddressPort):
            t = threading.Thread(target=host_to_host, args=(targetAddressPort, remoteAddressPort))
            t.start()
        else:
            sys.exit()
