# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from socket import *
import sys
import os

serverHost="127.0.0.1"
serverPort=int(sys.argv[1])
serverAddress=(serverHost,serverPort)

serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.bind(serverAddress)

while True:
    serverSocket.listen()
    #accept()第一个元素返回的是新的socket对象，服务器必须通过它与客户通信；第二个元素address是客户的Internet地址。
    clientSocket,clientAddress=serverSocket.accept()
    print(f"we have a new message from {clientAddress}")

    #show the message (HTTP request)
    msg=clientSocket.recv(1024)

    if msg:
        print(msg.decode())
        requested_resource = msg.decode().split('\n')[0].split((' '))[1][1:]
    #     #to do :analyse which file do we need to send
        print("the request want to visit the file:",requested_resource)
        if os.path.exists(requested_resource):
            print("resource exist")
            with open(requested_resource, "rb") as show_file:
                data=show_file.read()
                # print("已经运行到这一步")
                response="\nHTTP/1.1 200 OK\n\n"
                #to do: how to send a msg
                clientSocket.send(response.encode())#这行保留
                clientSocket.sendall(data)

        else:
            print("resource not exist")
            response="\nHTTP/1.1 404 not found\n\n"
            clientSocket.send(response.encode())
            continue

    #reply the message (make a HTTP response)

    # with open(requested_resource,"rb") as img_file:
    #     data=img_file.read()
    #     response="HTTP/1.1 200 OK\r\n"
    #     #to do: how to send a msg
    #     clientSocket.send(response.encode())
    #     clientSocket.send(data)

serverSocket.close()

#     # print("=============================")
#     # print(msg.decode())#这行保留
#     # print("=============================")
#     requested_resource=msg.decode().split('\n')[0].split((' '))[1][1:]
