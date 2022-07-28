import socket
import threading
from _thread import *

g_start_capture = False # 캡쳐 시작 대기 결정  
g_stop_sig = True
A = 0

HOST = '192.168.0.5'
PORT = 9999
lock = threading.Lock()

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print('>> Connect Server')

# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리       
def send_data(client_socket) :
    global g_start_capture
    global A
    if g_stop_sig == True:
        return 
    if g_start_capture == True : 
        with lock :
            g_start_capture = False    

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

        if str(data.decode()) == 'start' or str(data.decode()) == 'restart' :
            with lock :
                g_start_capture = True
                g_stop_sig = False   
            start_new_thread(send_data, (client_socket,))     
        elif str(data.decode()) == 'stop':
            with lock :
                g_stop_sig = True
        else : 
            print("not processing here")        
    except :
        print("error processing")
        break

client_socket.close()
