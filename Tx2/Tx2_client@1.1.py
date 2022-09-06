import json
from threading import Thread
import socket
import time

HOST = '155.230.25.98'
# HOST = '127.0.0.1'
PORT = 9999

# recivedData 전역변수 선언
global recivedData
# detector의 데이터를 서버로 전송


def send_detector_data(client, status: str, classType: str,  accord_x: float, accord_y: float):
    sendingData = json.dumps({
        "status": status,
        "from": "Detector",
        "data": {
                "class": classType,
                "accord_x": str(accord_x),
                "accord_y": str(accord_y)
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


def Detector_Client(client):
    while True:
        # recivedData 전역변수 사용
        global recivedData
        # dictionary type으로 받기
        recivedData = json.loads(client.recv(1024).decode())
        print(f"\n>> Received : \n{recivedData}")
        if (recivedData["status"] == "starting" or recivedData["status"] == "controlling_finished"):
            print("do something...")
            # detecting 중인 것을 서버에다가 알려야함.
            send_detector_data(client,  status="detecting", classType="resistor",
                               accord_x=0, accord_y=0)
            time.sleep(3)
            # 작업 코드 추가하면됩니다....
            send_detector_data(client, status="detecting_finished", classType="resistor",
                               accord_x=30, accord_y=20)
            print("finished")


if (__name__ == "__main__"):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print('>> Connect Server')
    send_connect_msg(client)
    Detector_Client = Thread(name="Detector_Client", target=Detector_Client,
                             args=(client,), daemon=True)
    Detector_Client.start()

    while True:
        inputData = input('')
        if inputData == 'quit':
            print("exit client")
            break
        elif inputData == 'clear':
            send_detector_data(client, status=recivedData["status"], classType="none",
                               accord_x=0, accord_y=0)
        elif inputData == 'td':
            send_detector_data(client, status=recivedData["status"], classType="resistor",
                               accord_x=60, accord_y=60)
    client.close()
