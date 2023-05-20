# -*- encoding:utf-8 -*-
from threading import Thread
import time
from socket import *
host='127.0.0.1'
port=9999
filename='example1.mp4'
send_user='A'

def UDP_receiver(host,port,send_user):
    buffer = 1024
    a = 10
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((host, port))
    addr = (host, port)
    # 1.receive the filename
    data, addr = s.recvfrom(buffer)
    print('Received File:', data.decode().strip())
    dataname = send_user + '_' + data.decode().strip()
    f = open(dataname, 'wb')

    # 2. write the content into the file
    data, addr = s.recvfrom(buffer)
    try:
        while (data):
            f.write(data)
            s.settimeout(2)
            data, addr = s.recvfrom(buffer)
    except timeout:
        f.close()
        s.close()

        print('File downloaded')

def UDP_sender(host,port,filename):
    buffer = 1024
    s = socket(AF_INET, SOCK_DGRAM)
    addr = (host, port)
    # sender_addr = (serverHost, udp_server_port)
    # 1.send the filenme
    s.sendto(filename.encode(), addr)
    # send the filecontent
    file = open(filename, 'rb')
    data = file.read(buffer)
    while data:
        send_bytes = s.sendto(data, addr)
        if send_bytes:
            print(f'sending a package, size = {send_bytes}......')
            data = file.read(buffer)
    s.close()
    file.close()

t1=Thread(target=UDP_sender,args=((host,port,filename)))
t2=Thread(target=UDP_receiver,args=((host,port,send_user)))
t2.start()
t1.start()
time.sleep(5)
t1.join()
t2.join()
# main()
# print_hello()