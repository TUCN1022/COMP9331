# -*- encoding:utf-8 -*-
import random
import os

def edg(self,fileid:int,dataamount:int)->str:

    # if not isinstance(dataamount,int) or not isinstance(fileid,int):
    #     return 'the fileID or dataAmount are not integers, you need to specify the parameter as integers'
    with open(f'supersmartwatch-{fileid}.txt','w+') as file:
        for i in range(dataamount):
            file.write(f'{random.randint(1,100)}')
    return 'data generation done'




# with open("supersmartwatch-1.txt",'r') as file:
#     data=file.readlines()
#     print(type(data))
if os.path.exists("supersmartwatch-2.txt")==False:
    print(1)



elif "EDG" in message:
    print("[recv] New EDG request")
    req, id, amount = message.split(' ')
    try:
        id = int(id)
        amount = int(amount)
    except ValueError:
        print("the fileID or dataAmount are not integers, you need to specify the parameter as integers")
    except amount == '' or id == '':
        print('EDG command requires fileID and dataAmount as arguments.')
    else:
        self.edg(id, amount)


    # def edg(self,fileid: int, dataamount: int) -> str:
    #     if self.name=='':
    #         message="not login in"
    #     # if not isinstance(dataamount,int) or not isinstance(fileid,int):
    #     #     return 'the fileID or dataAmount are not integers, you need to specify the parameter as integers'
    #     else:
    #         with open(f'{self.name}-{fileid}.txt', 'w+') as file:
    #             for i in range(dataamount):
    #                 file.write(f'{random.randint(1, 100)}\n')
    #         message = 'data generation done'
    #
    #     self.clientSocket.send(message.encode())

    elif message == "CHECK":
    print("[recv] New CHECK request")
    self.check_account_num()

elif message == "INFO":
    print("[recv] New INFO request")
    self.INFO()


    def check_account_num(self):
        num = str(len(ClientThread.accounts))
        message = num
        self.clientSocket.send(message.encode())

    def info(self):
        message = ''
        for i in range(len(ClientThread.accounts)):
            message += ClientThread.accounts[i] + ' '
        message += '\n'
        message += f"The user is {self.name}."
        self.clientSocket.send(message.encode())

local_addr = ('', udp_server_port)
udp_socket.bind(local_addr)
rs_data = udp_socket.recvfrom(2048)
rs_message = rs_data[0]  # receive data
rs_address = rs_data[1]  # receive address (ip,port)
rs_message = rs_message.decode()
save_name = devicename + '_' + filename
with open(save_name, 'w+') as save_file:
    save_file.write(rs_message)
udp_socket.close()

if judge == "True":
    buffer = 1024
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    sender_addr = (serverHost, udp_server_port)
    # 1.send the filenme
    udp_socket.sendto(filename.encode(), sender_addr)
    # send the filecontent
    file = open(filename, 'rb')
    data = file.read(buffer)
    while data:
        send_data = udp_socket.sendto(data, sender_addr)
        if send_data:
            print(f'sending a package, size = {send_data}......')
            data = file.read(buffer)
    udp_socket.close()
    file.close()

    print('finish sending，start receive')

    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((host, udp_server_port))
    addr = (host, udp_server_port)
    print(1)
    # 1.receive the filename
    data, addr = s.recvfrom(buffer)
    print('Received File:', data.decode().strip())
    dataname = send_user + '_' + data.strip()
    print(dataname)
    f = open(dataname, 'wb')
    print(2)

    # 2. write the content into the file
    data, addr = udp_socket.recvfrom(buffer)
    print(3)
    try:
        while (data):
            f.write(data)
            udp_socket.settimeout(2)
            data, addr = udp_socket.recvfrom(buffer)
    except timeout:
        f.close()
        udp_socket.close()
        print('File downloaded')