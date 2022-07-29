import socket
from _thread import *

HOST = '192.168.0.5'
PORT = 9999

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print ('>> Connect Server')
     
while True:  
    try:
        message = input("input : start or stop : ")
        if message == 'start' or message == 'stop':
            client_socket.send(message.encode())
        else :
            print("wrong input! do it again \n")   
    except :
        print("error processing")
        break
        
client_socket.close()
