import socket
from threading import Thread
import json

HOST = '155.230.25.98'
# HOST = '127.0.0.1'
PORT = 9999

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST, PORT))


# 서버로부터 메세지를 받는 메소드
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리
def recv_data(client) :
    while True :
        recivedData = client.recv(1024)
        # print(recivedData.decode())
        print(f">> Received : \n{recivedData.decode()}")

# start_new_thread(recv_data, (client,))
socketClient=Thread(name="socketClient", target=recv_data, args=(client,),daemon=True)
socketClient.start()
print ('>> Connect Server')

while True:
    sendingData = input('')
    if sendingData == 'quit':
        print("exit client")
        break

    sendingData = json.dumps({
        "from" : "detector(Rpi)",
        "msg" : sendingData
    },sort_keys=True,indent=4)

    # print(sendingData)
    client.send(sendingData.encode())
client.close()
