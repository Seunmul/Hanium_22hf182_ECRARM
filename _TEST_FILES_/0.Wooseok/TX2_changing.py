import socket
from _thread import *
import time

g_start_capture = False # 캡쳐 시작 대기 결정  
g_stop_sig = True
A = 0   
B = 0

HOST = '192.168.0.165'
PORT = 9999
lock = allocate_lock()

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print('>> Connect Server')

# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리       
def send_data(client_socket) :
    global g_start_capture, A, B, g_stop_sig
    if g_start_capture == True : 
        with lock :
            g_start_capture = False    

        # 소자가 없으면 웹에 프로세스 종료 메시지 송신, 종료,
        # 이미지 인식 후 인식된 값이 있어야 함
        # 오류로 인한, 소자를 순간적으로 인식하지 못하는, 프로세스 종료를 막기 위한 방안이 필요
        # if num_objects == 0 : or file 에서 받아오는 값이 없다면 실행하는 것도 괜찮을 듯
        if B == 2 :
            client_socket.send("stop".encode()) # stop 을 보내면 다른
            print("no element found")
            with lock:
                g_stop_sig = True
            B=B-3
            return
        B=B+1    

        #이미지 인식 및 좌표값 및 종류 획득
        #반복문으로 이 부분 처리, 잡히는 물체가 없으면 continue, 있으면 send
        # while True: 
        if A % 2 == 0:
            message = '800 5 44 85 62'
        else :
            message = '400 12 19 55 5'
        A = ( A % 2 ) + 1     
        client_socket.send(message.encode())      
    return          

while True :
    try :
        data = client_socket.recv(1024) # start stop restart 받음
        print("recive : ",repr(data.decode()))

        if str(data.decode()) == 'stop' :
            with lock :
                g_stop_sig = True
            continue    
        elif str(data.decode()) == 'start' :
            with lock :
                g_stop_sig = False
                g_start_capture = True
        elif str(data.decode()) == 'restart' :
            with lock :
                g_start_capture = True

        if g_stop_sig == True :
            print("stop signal is already recived, "+data.decode()+" message is ignored\n")
            continue

        time.sleep(2)

        start_new_thread(send_data, (client_socket,))
    except :
        print("error processing")
        break

client_socket.close()
