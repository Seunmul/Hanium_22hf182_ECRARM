import socket
import threading
import time
from _thread import *
import sys
import RPi.GPIO as GPIO


sys.path.append("../step_test")
import step_A4988_test1 as stepControl


HOST = '192.168.0.5'
PORT = 9999
lock = threading.Lock()

g_send_message = False
g_stop_sig = True

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print ('>> Connect Server')
#CONTROL SETUP PARAMS
STEPPIN = 29
DIRPIN = 31
ENPIN = 33
FREQ= 60
PINS = [STEPPIN,DIRPIN,ENPIN,35]
stepControl.__SETUP__(PINS)

# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리
def send_data(client_socket) :
    global g_send_message
    if g_stop_sig == True:
        return 
    if g_send_message == True :
        with lock :
            g_send_message = False

        message = 'restart'
        client_socket.send(message.encode())
    return

while True :
    try:
        data = client_socket.recv(1024)  # start stop 좌표값 받음
        print("recive : ",repr(data.decode()))

        if str(data.decode()) == 'start':
            print("not processing here\n")
            with lock:
                g_stop_sig = False
            continue
        elif str(data.decode()) == 'stop':
            print("pause processing\n")    
            with lock :
                g_stop_sig = True
            continue

        first_move = list(data.decode().split())

        with lock :
            print("processing==>")
            time.sleep(2)
            print(" "+first_move[0]+" "+first_move[1]+" "+first_move[2]+" "+first_move[3]+" "+first_move[4]+"\n")
            stepControl.__CONTORL__(first_move[0],STEPPIN,DIRPIN,ENPIN)
            g_send_message = True
            start_new_thread(send_data, (client_socket,))
    except KeyboardInterrupt:
        print("error processing")
        break

GPIO.cleanup()
client_socket.close()  