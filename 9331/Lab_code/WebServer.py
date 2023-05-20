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
    clientSocket,clientAddress=serverSocket.accept()
    print(f"we have a new message from {clientAddress}")

    msg=clientSocket.recv(1024)

    if msg:
        print(msg.decode())
        requested_resource = msg.decode().split('\n')[0].split((' '))[1][1:]

        print("the request want to visit the file:",requested_resource)
        if os.path.exists(requested_resource):
            print("resource exist")
            with open(requested_resource, "rb") as show_file:
                data=show_file.read()

                response="\nHTTP/1.1 200 OK\n\n"

                clientSocket.send(response.encode())
                clientSocket.sendall(data)

        else:
            print("resource not exist")
            response="\nHTTP/1.1 404 not found\n\n"
            clientSocket.send(response.encode())
            continue



serverSocket.close()


