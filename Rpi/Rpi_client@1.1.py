import json
from threading import Thread
import socket
import time

HOST = '155.230.25.98'
# HOST = '127.0.0.1'
PORT = 9999

# recivedData 전역변수 선언
global recivedData
# controller의 데이터를 서버로 전송


def send_controller_data(client, status: str, X: float, Y: float, Z: float, W: float, R: float):
    sendingData = json.dumps({
        "status": status,
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


def Controller_Client(client):
    while True:
        # recivedData 전역변수 사용
        global recivedData
        # dictionary type으로 받기
        recivedData = json.loads(client.recv(1024).decode())
        print(f"\n>> [C] received : \n{recivedData}")
        if (recivedData["status"] == "detecting_finished"):
            print("do something...")
            # detecting 중인 것을 서버에다가 알려야함.
            send_controller_data(client, status="controlling",
                                 X=0, Y=0, Z=0, W=0, R=0)
            time.sleep(3)
            # 작업 코드 추가하면됩니다....
            send_controller_data(client, status="controlling_finished",
                                 X=10, Y=20, Z=30, W=40, R=50)
            print("finished")


if (__name__ == "__main__"):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print('>> Connect Server')
    send_connect_msg(client)
    Controller_Client = Thread(name="Controller_Client", target=Controller_Client,
                               args=(client,), daemon=True)
    Controller_Client.start()

    while True:
        inputData = input('')
        if inputData == 'quit':
            print("exit client")
            break
        elif inputData == 'clear':
            send_controller_data(client, status=recivedData["status"],X=0, Y=0, Z=0, W=0, R=0)
        elif inputData == 'td':
            send_controller_data(client, status=recivedData["status"],X=5, Y=5, Z=5, W=5, R=5)

    client.close()
