import json
from threading import Thread
import socket

HOST = '155.230.25.98'
# HOST = '127.0.0.1'
PORT = 9999

# detector의 데이터를 서버로 전송


def send_detector_data(client, classType: str, accord_x: float, accord_y: float):
    sendingData = json.dumps({
        "from": "Detector",
        "data": {
                "class": classType,
                "x": str(accord_x),
                "y": str(accord_y)
        }

    }, sort_keys=True, indent=4)
    # print(f'>> send Data : {sendingData}')
    client.send(sendingData.encode())
    return

# connect 메시지 전송 및 이니셜라이즈


def send_connect_msg(client):
    sendingData = json.dumps({
        "from": "Detector",
        "data": "connect"

    }, sort_keys=True, indent=4)
    client.send(sendingData.encode())
    return


def recv_data(client):
    while True:
     # dictionary type으로 받기
        recivedData = json.loads(client.recv(1024).decode())
        print(f"\n>> Received : \n{recivedData}")


if (__name__ == "__main__"):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print('>> Connect Server')
    send_connect_msg(client)
    socketClient = Thread(name="socketClient", target=recv_data,
                          args=(client,), daemon=True)
    socketClient.start()

    while True:
        sendingData = input('')
        if sendingData == 'quit':
            print("exit client")
            break
        send_detector_data(client, classType="resistor", accord_x=30, accord_y=20)
        
    client.close()
