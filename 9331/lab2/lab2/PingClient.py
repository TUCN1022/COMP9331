#python version is 3


import socket
import sys
import time


hostname=sys.argv[1]

port=sys.argv[2]
rtts=[]
port=int(port)
for i in range(3331,3346):
    address=(hostname,port)
    #address=('127.0.0.1',2048)
    
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print_time=time.strftime('%Y-%m-%d %H-%M-%S')
    message=f"{i} {print_time}\n"
    sock.sendto(message.encode(),address)
    sock.settimeout(0.6)
    try:
        #todo
        send_time=time.time()
        
        response=sock.recv(1024)
        
        get_time=time.time()
        rtt=(get_time-send_time)*1000
        rtts.append(rtt)
        #print(rtt)
        print("ping to {},seq={},rtt={:.3f}ms. ".format(hostname,i,rtt))
        #print(f"ping to {hostname},seq={i},rtt={rtt}ms. ")
    except:
        print("ping to {},seq={}, time out. ".format(hostname,i))

    sock.close()

MIN_rtt=min(rtts)
MAX_rtt=max(rtts)
AVG_rtt=sum(rtts)/len(rtts)

print('MIN_RTT:{:.3f}ms'.format(MIN_rtt))
print('MAX_RTT:{:.3f}ms'.format(MAX_rtt))
print('AVG_RTT:{:.3f}ms'.format(AVG_rtt))
