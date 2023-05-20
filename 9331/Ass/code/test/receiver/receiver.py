# -*- encoding:utf-8 -*-
from socket import *
host='127.0.0.1'
port=9999
send_user='A'

buffer=1024
s = socket(AF_INET, SOCK_DGRAM)
s.bind((host, port))
addr = (host, port)
print(1)
# 1.receive the filename
data, addr = s.recvfrom(buffer)
print('Received File:', data.decode().strip())
dataname = send_user + '_' + data.decode().strip()
print(dataname)
f = open(dataname, 'wb')
print(2)

# 2. write the content into the file
data, addr = s.recvfrom(buffer)
print(3)
try:
    while (data):
        f.write(data)
        s.settimeout(2)
        data, addr = s.recvfrom(buffer)
except timeout:
    f.close()
    s.close()
    print('File downloaded')