import os
from socket import *
from threading import Thread
import sys, select
from collections import defaultdict
import datetime
import time
import random
import json

'''
the python version is python3
read the arguments in the terminal, there are two arguments:
1.the server's port
2. the time to block the user to login in 
'''
if len(sys.argv) != 3:
    print("\n===== Error usage, python3 server.py SERVER_PORT Time_to_Block======\n")
    exit(0)
serverHost = "127.0.0.1"
serverPort = int(sys.argv[1])
serverAddress = (serverHost, serverPort)

# define socket for the server side and bind address
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(serverAddress)


# create a multi-thread server
class ClientThread(Thread):
    '''
    set the argument 'num_of_user' to count how many user are using in the server,and the list account to store the users' name, login_block store those user who is blocking because of the wrong password, the time is the time they can relogin.
    The __init__ function store the basic auguments in the server:
    login_failed_times used to count the times that user print the wrong password
    name sore the user name who is using
    '''
    num_of_user = 0
    accounts = []
    login_block = defaultdict(datetime.datetime)

    def __init__(self, clientAddress, clientSocket):
        Thread.__init__(self)
        self.clientAddress = clientAddress
        self.clientSocket = clientSocket
        self.login_failed_times = defaultdict(int)
        # self.login_block = defaultdict(datetime.datetime)
        self.name = ''
        self.block_time = int(sys.argv[2])
        print("===== New connection created for: ", clientAddress)
        self.clientAlive = True

    def run(self):
        message = ''

        while self.clientAlive:
            data = self.clientSocket.recv(1024)
            message = data.decode()

            # if the message from client is empty, the client would be off-line then set the client as offline (alive=Flase)
            if message == '':
                self.clientAlive = False
                print("===== the user disconnected - ", clientAddress)
                break

            '''
            if the client message include the relative request , it will run the function about it
            '''
            if 'login' in message:
                print("[recv] New login request")
                self.process_login(message)

            elif "EDG" in message:
                print("[recv] New EDG request")
                message = self.name
                self.clientSocket.send(message.encode())

            elif "UED" in message:
                print(f"[recv] Edge device {self.name} issued UED command")
                print(f'A data file is received from edge device {self.name}')
                try:
                    req, id = message.split(' ')
                    id = int(id)
                except ValueError:
                    print("the fileID is not integers, you need to specify the parameter as integers")
                except id == '':
                    print('DTE command requires fileID and dataAmount as arguments.')
                else:
                    message = self.name
                    self.clientSocket.send(message.encode())

            elif "uploadingdata" in message:
                data = message.split(' ')
                fileid = data[1]
                data = data[2:]
                with open(f"{self.name}-{fileid}.txt", 'w+') as file:
                    for item in data:
                        file.write(item)
                message = f"The file with ID of {fileid} has been received, upload-log.txt file has been updated"
                print(message)
                self.clientSocket.send(message.encode())
                dataAmount = len(data)
                self.uploadlog(fileid, dataAmount)

            elif "SCS" in message:
                print("[recv] New SCS request")
                try:
                    req, id, operation = message.split(' ')
                    id = int(id)
                except ValueError:
                    message = "the fileID are not integers, you need to specify the parameter as integers"
                    self.clientSocket.send(message.encode())
                except operation == '' or id == '':
                    message = '“fileID is missing or fileID should be an integer'
                    self.clientSocket.send(message.encode())
                except FileNotFoundError:
                    message = "fileID is missing or fileID should be an integer"
                    self.clientSocket.send(message.encode())
                else:
                    print(f'Edge device {self.name} requested a computation operation on the file with ID of {id}')
                    self.scs(id, operation)

            elif "DTE" in message:
                try:
                    req, id = message.split(' ')
                    id = int(id)
                except ValueError:
                    print("the fileID is not integers, you need to specify the parameter as integers")
                except id == '':
                    print('DTE command requires fileID and dataAmount as arguments.')
                except os.path.exists(self.name + "-" + id + ".txt") == False:
                    message = "the file is not exist in the server"
                    self.clientSocket.send(message.encode())
                else:
                    print(f"Edge device {self.name} issued DTE command, the file ID is {id}")
                    self.dte(id)

            elif message == "AED":
                message = ''
                print(f"The edge device {self.name} issued AED command")
                try:
                    with open('edge_device_log.txt', 'r') as AED_file:
                        data = AED_file.readlines()
                        for item in data:
                            no, timestamp, username, host, port = item.split('; ')
                            if self.name == username:
                                continue
                            message += f'{username}; {host}; {port}; {timestamp}\n'
                except FileNotFoundError:
                    message = 'no other active edge devices'
                    print(message)
                else:
                    print(f'Return messages: {message}')
                    if message=='':
                        message='None'
                    self.clientSocket.send(message.encode())

            elif message == "OUT":
                ClientThread.num_of_user-=1
                ClientThread.accounts.remove(self.name)
                print(f"[recv] {self.name} exited the edge network")
                self.clientAlive = False

                findout = False
                with open('edge_device_log.txt', 'r') as AED_file:
                    data = AED_file.readlines()
                with open('edge_device_log.txt', 'w+') as AED_file:
                    for item in data:
                        if item=='\n':
                            continue
                        no, timestamp, name, host, port = item.split("; ")
                        no = int(no)
                        if self.name == name:
                            findout = True
                            continue
                        elif self.name != name and findout == False:
                            AED_file.write(f"{no}; {timestamp}; {name}; {host}; {port}\n")
                        elif self.name != name and findout == True:
                            AED_file.write(f"{no - 1}; {timestamp}; {name}; {host}; {port}\n")
                message = f"Bye, {self.name}!"
                self.clientSocket.send(message.encode())

            elif "UVF" in message:
                findout = False
                reply_message = f'{self.name} False null null'
                req, devicename = message.split()
                with open('edge_device_log.txt', 'r') as file:
                    data = file.readlines()
                    for item in data:
                        no, timestamp, name, host, port = item.split('; ')
                        if name == devicename:
                            findout = True
                            reply_message = f'{self.name} {findout} {host} {port}'  # str(findout)+' '+host+' '+port
                            break

                self.clientSocket.send(reply_message.encode())

            # if the message not include any relative request, it will send the reply message that the request can not understand
            else:
                print("[recv] " + message)
                print("[send] Cannot understand this message")
                message = 'Cannot understand this message'
                self.clientSocket.send(message.encode())

    '''
    login relative function. Firstly, it will split the username and password from message, then it will check whether the user name is block, if not,it will check the user file to finish the login. 
    every time the password is fault, it will do the record， when the fault time get the block times, it will prevent the user from logging in for ten seconds
    '''

    def process_login(self, message):
        action, username, password = message.split(" ")
        # if the username is in block,then display and quit
        if username in ClientThread.login_block and datetime.datetime.now() < ClientThread.login_block[username]:
            sleeptime = (datetime.datetime.strptime(
                datetime.datetime.strftime(ClientThread.login_block[username], "%Y/%m/%d %H:%M:%S"),
                "%Y/%m/%d %H:%M:%S") - datetime.datetime.strptime(
                datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S")).seconds
            reply_message = f"login fail, the user is block now,please wait for {sleeptime} sec."
            print('[send] ' + reply_message)
            self.clientSocket.send(reply_message.encode())
            time.sleep(sleeptime)
            return
        # open credentials to check
        with open('credentials.txt', 'r') as credentials_file:
            credentials_content = credentials_file.read()
        login_success = False

        for row in credentials_content.split('\n'):
            try:
                row_username, row_password = row.split(' ')
            except:
                continue
            if username == row_username and password == row_password:
                self.name = username
                login_success = True
                ClientThread.accounts.append(self.name)

        if login_success:
            reply_message = 'admin login success.'
            ClientThread.num_of_user += 1
            now = datetime.datetime.now()
            timestamp = now.strftime("%d %B %Y %H:%M:%S")
            with open("edge_device_log.txt", 'a+') as devicelog_file:
                content = f"{ClientThread.num_of_user}; {timestamp}; {self.name}; {serverHost}; {serverPort}\n"
                devicelog_file.write(content)
        else:
            self.login_failed_times[username] += 1
            reply_message = f'admin login failed. user:{username} failed {self.login_failed_times[username]} times. If fail {self.block_time} times, it will bolck.'
            print(reply_message)
            if self.login_failed_times[username] == self.block_time:
                reply_message += f'\n failed time reach {self.login_failed_times[username]}, it will block 10 sec'
                self.login_failed_times[username] = 0
                ClientThread.login_block[username] = datetime.datetime.now() + datetime.timedelta(seconds=10)

        print('[send] ' + reply_message);
        self.clientSocket.send(reply_message.encode())

    # do the SCS calculation, if the operation is not exist, reply the operation request is not exist
    def scs(self, fileid, operation):
        if self.name == '':
            message = "not login in"
        else:
            try:
                with open(f"{self.name}-{fileid}.txt", 'r') as file:
                    data = file.readlines()
            except FileNotFoundError:
                message = "the file is not in server, so can not operation."
            else:

                for i in range(len(data)):
                    data[i] = int(data[i])
                if operation == "SUM":
                    message = f'{operation} computation has been made on edge device {self.name} data file (ID:{fileid}), the result is ' + str(
                        sum(data))
                elif operation == "AVERAGE":
                    message = f'{operation} computation has been made on edge device {self.name} data file (ID:{fileid}), the result is ' + (
                        str(sum(data) / len(data)))
                elif operation == "MAX":
                    message = f'{operation} computation has been made on edge device {self.name} data file (ID:{fileid}), the result is ' + str(
                        max(data))
                elif operation == "MIN":
                    message = f'{operation} computation has been made on edge device {self.name} data file (ID:{fileid}), the result is ' + str(
                        min(data))
                else:
                    message = 'The operation is not exist'
                    print(f'Return message: {message}')
        self.clientSocket.send(message.encode())

    # delete the file in the server and update the delete_log file
    def dte(self, fileID):
        if self.name == '':
            message = "not login in"

        else:
            filename = f"{self.name}-{fileID}.txt"
            if os.path.exists(filename) == False:
                message = '“the file does not exist at the server side'
            else:
                with open(filename, 'r+') as file:
                    data = file.readlines()
                    datamat = len(data)

                    now = datetime.datetime.now()
                    timestamp = now.strftime("%d %B %Y %H:%M:%S")
                    content = f"{self.name}; {timestamp}; {fileID}; {datamat}\n"
                    with open("deletion_log.txt", 'a') as delete_file:
                        delete_file.write(content)
                os.remove(filename)

                message = f"The file with ID of {fileID} from edge device {self.name} has been deleted, \
                deletion log file has been updated"
                print(f'Return message: {message}')

        self.clientSocket.send(message.encode())

    # the uploadlog function is relative to the UED.
    # after the file upload to sever, the server will run this function to update the upload_log file
    def uploadlog(self, fileID, dataAmount):
        dt_now = datetime.datetime.now().strftime("%d %B %Y %H:%M:%S")
        with open("upload_log.txt", 'a+') as file:
            content = f"{self.name}; {dt_now}; {fileID}; {dataAmount}\n"
            file.write(content)


print("\n===== Server is running =====")
print("===== Waiting for connection request from clients...=====")

while True:
    serverSocket.listen()
    clientSockt, clientAddress = serverSocket.accept()
    clientThread = ClientThread(clientAddress, clientSockt)
    clientThread.start()
