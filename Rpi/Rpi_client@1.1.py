import json
from threading import Thread
import socket

HOST = '155.230.25.98'
# HOST = '127.0.0.1'
PORT = 9999

# controller의 데이터를 서버로 전송


def send_controller_data(client, X: float, Y: float, Z: float, W: float, R: float):
    sendingData = json.dumps({
        "from": "Controller",
        "data": {
            "X_Axis": str(X),
            "Y_Axis": str(Y),
            "Z_Axis": str(Z),
            "W_Axis": str(W),
            "R_Axis": str(R)
        }

    }, sort_keys=True, indent=4)
    # print(f'>> send Data : {sendingData}')
    client.send(sendingData.encode())
    return

# connect 메시지 전송 및 이니셜라이즈


def send_connect_msg(client):
    sendingData = json.dumps({
        "from": "Controller",
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
        inputData = input('')
        if inputData == 'quit':
            print("exit client")
            break
        send_controller_data(client, X=10, Y=20, Z=30, W=40, R=50)

    client.close()
