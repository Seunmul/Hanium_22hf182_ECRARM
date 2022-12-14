import socket
import time
import sys
from _thread import *

# ../basic-gpio-test/servoTest_input.py import
# print(sys.path)
sys.path.append("../basic-gpio-test")
import servoTest_input as servoControl
#

# HOST = '127.0.0.1'
HOST = '192.168.0.165'
PORT = 9999


client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


# 서버로부터 메세지를 받는 메소드
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리
def recv_data(client_socket) :
    while True :
        data = client_socket.recv(1024)

        print("from server recive : ",repr(data.decode()))


# start_new_thread(recv_data, (client_socket,))
print ('>> Connect Server')
client_socket.send("client connected, send msg(degree, 0 to 180)".encode())
while True:
    data = client_socket.recv(1024)
    print("[from server] recived : ",repr(data.decode()))
    if data.decode() == 'quit':
        client_socket.send('closed, press any key'.encode())
        break
    message = str('done')
    # if message == 'quit':
    #     close_data = message
    #     break
    print("processing==>")
    time.sleep(0.2)
    try:
        if(int(data.decode())>=0 & int(data.decode())<=180):
            servoControl.__CONTROL__(data.decode())
    except ValueError:
        message = str('wrong input')
    finally : 
        print("end==>\n")
        client_socket.send(message.encode())

servoControl.__CLEAR_GPIO__()

client_socket.close()
