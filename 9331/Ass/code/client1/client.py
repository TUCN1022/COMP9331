import time
from threading import Thread
from socket import *
import sys
import random
import os
import select

'''
the python version is python3
'''

#UDP_receiver function used to receive the p2p file. The arguments include the receiver's host,port and the sender's name.
#it will generate a file consist by the user name and the file name.
def UDP_receiver(host,port,send_user):
    buffer=1024
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


#UDP_sender function used to send the p2p file. The arguments include the sender's host,port and the file name.
#it will send the file in the client side.
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


#the edg function is used to generate the digital file. It include the dataamount numbers.
def edg(name, fileid: int, dataamount: int) -> str:
    if name == '':
        message = "not login in"
    else:
        with open(f'{name}-{fileid}.txt', 'w+') as file:
            for i in range(dataamount):
                file.write(f'{random.randint(1, 100)}\n')
        message = f'data generation done, {dataamount} data samples have been generated and stored in the file {name}-{fileid}.txt'
    print(message)

#get the client.py arguments
if len(sys.argv) != 4:
    print("\n===== Error usage, python3 clientclient.py SERVER_IP SERVER_PORT  UDP_SERVER_PORT======\n")
    exit(0)
serverHost = sys.argv[1]
serverPort = int(sys.argv[2])
udp_server_port=int(sys.argv[3])
serverAddress = (serverHost, serverPort)

# define a socket for the client side, it would be used to communicate with the server
clientSocket = socket(AF_INET, SOCK_STREAM)

# build connection with the server and send message to it
clientSocket.connect(serverAddress)

while True:
    #get the input message
    message = input("===== Please type any messsage you want to send to server (login/EDG/UED/SCS/DTE/AED/UVF/OUT): =====\n")
    if message== 'login':
        username=input("username: ")
        password=input("password: ")
        message=f"login {username} {password}"
        clientSocket.sendall(message.encode())
        data = clientSocket.recv(2048)
        receivedMessage = data.decode()
        print(receivedMessage)

    #generate edge data
    elif 'EDG' in message:
        try:
            req, id, amount = message.split(' ')
            id = int(id)
            amount = int(amount)
        except ValueError:
            print("the fileID or dataAmount are not integers, you need to specify the parameter as integers")
        except amount == '' or id == '':
            print('EDG command requires fileID and dataAmount as arguments.')
        else:
            message=f"EDG {id} {amount}"
            print(f"The edge device is generating {amount} data samples…")
            clientSocket.sendall(message.encode())
            data = clientSocket.recv(2048)
            receivedMessage = data.decode()
            name=receivedMessage
            #use edg function
            edg(name,id, amount)

    #if the request 'UED' in message, it will send first request to get the user name,
    # then it will consist the user name and the file id and the file data as the message to send to server.
    elif 'UED' in message:#上传边缘数据
        try:
            req, fileid = message.split(' ')
            fileid = int(fileid)
        except ValueError:
            print("the fileID is not integers, you need to specify the parameter as integers")
        else:
            message=f"UED {fileid}"
            clientSocket.sendall(message.encode())
            data = clientSocket.recv(2048)
            receivedMessage = data.decode()
            name = receivedMessage
            if name!='':
                try:
                    with open(f"{name}-{fileid}.txt") as file:
                        data=file.readlines()
                except FileNotFoundError:
                    print(f'{name}-{fileid}.txt is not exist in the client side.')
                else:
                    message=f"uploadingdata {fileid}"
                    for item in data:
                        message+=" "+item
                    # print(message)
                    clientSocket.sendall(message.encode())
                    data = clientSocket.recv(2048)
                    receivedMessage = data.decode()
                    if 'has been updated' in receivedMessage:
                        print(f"Data file with ID of {fileid} has been uploaded to server.")

    #request server to do the calculation
    elif 'SCS' in message:#服务器计算服务
        try:
            req, fileid, operation= message.split(' ')
            fileid = int(fileid)
        except ValueError:
            print("the fileID is not integers or the operation is null, you need to specify the parameter as integers or add the operation")
        else:
            message = f"SCS {fileid} {operation}"
            clientSocket.sendall(message.encode())
            data = clientSocket.recv(2048)
            receivedMessage = data.decode()
            receivedMessage=receivedMessage.split()
            if receivedMessage[0] not in ['SUM','MIN','MAX','AVERAGE']:
                printout="operation has error"
            else:
                printout=f'Computation ({receivedMessage[0]}) result on the file {receivedMessage[-5][:-1]} returned from the server is: {receivedMessage[-1]}'
            print(printout)

    #request server to delete the relative file
    elif 'DTE' in message:
        try:
            req, fileid = message.split(' ')
            fileid = int(fileid)
        except ValueError:
            print("the fileID is not integers, you need to specify the parameter as integers")
        else:
            message = f"DTE {fileid}"
            clientSocket.sendall(message.encode())
            data = clientSocket.recv(2048)
            receivedMessage = data.decode()
            # print(receivedMessage)

    #request server to get the active user
    elif message=='AED':
        message = "AED"
        clientSocket.sendall(message.encode())
        data = clientSocket.recv(2048)
        receivedMessage = data.decode()
        print(receivedMessage)

    #quit out of the server
    elif message=="OUT":
        message = "OUT"
        clientSocket.sendall(message.encode())
        data = clientSocket.recv(2048)
        receivedMessage = data.decode()
        print(receivedMessage)
        break

    #ask for p2p file transger
    elif "UVF" in message:
        try:
            req, devicename, filename = message.split(' ')
            file=open(filename,'r')

        except ValueError:
            print("the arguments is not enough")
        except FileNotFoundError:
            print('the file you want to send is not exists!')
        else:
            file.close()
            message=f'UVF {devicename}'
            clientSocket.sendall(message.encode())
            data = clientSocket.recv(2048)
            receivedMessage = data.decode()
            send_user,judge,host,port=receivedMessage.split()

            if judge=="True":
                t1 = Thread(target=UDP_receiver, args=((host, udp_server_port, send_user)))
                t2 = Thread(target=UDP_sender, args=((serverHost, udp_server_port, filename)))

                t1.start()
                t2.start()
                time.sleep(10)
                t1.join()
                t2.join()

            else:
                print(f'{devicename} is offline.')

    # parse the message received from server and take corresponding actions
    elif receivedMessage == "":
        print("[recv] Message from server is empty!")
    else:
        print("Error. Invalid command!")

# close the socket
clientSocket.close()

