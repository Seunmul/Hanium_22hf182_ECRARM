import socket
from _thread import *

HOST = '192.168.0.5'
PORT = 9999

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print ('>> Connect Server')
     
def send_message(client_socket):  
    while True:
        try:
            message = input("input : start or stop : ")
            if message == 'start' or message == 'stop':
                client_socket.send(message.encode())
            else :
                print("wrong input! do it again \n")   
        except :
            print("error processing")
            return

start_new_thread(send_message, (client_socket,))  

while True:
    try :
        data = client_socket.recv(1024)
        if str(data.decode()) == "stop" :
            print("\n============================================")
            print("there can be no more elements in the board")
            print('be careful what you type')
            print("<start or stop>")
    except :
        print("error processing")
        break  
        

client_socket.close()