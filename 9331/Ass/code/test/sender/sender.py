# -*- encoding:utf-8 -*-
from socket import *
host='127.0.0.1'
port=9999
filename='example1.mp4'

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