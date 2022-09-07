import json
from threading import Thread
import socket
import time

HOST = '155.230.25.98'
# HOST = '127.0.0.1'
PORT = 9999

# receivedData 전역변수 선언
global receivedData
receivedData = {
    "Controller": {
        "connect": True,
        "data": {
            "R_Axis": 0,
            "W_Axis": 0,
            "X_Axis": 0,
            "Y_Axis": 0,
            "Z_Axis": 0
        }
    },
    "Detector": {
        "connect": False,
        "data": {
            "class": "none",
            "x": 0,
            "y": 0
        }
    },
    "Web": {
        "bridgeConnect": False,
        "data": ""
    },
    "status": "initializing"
}

# detector의 데이터를 서버로 전송
def send_detector_data(client, status: str, classType: str,  accord_x: float, accord_y: float):
    sendingData = json.dumps({
        "status": status,
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
        "status": "connecting",
        "from": "Detector",
        "data": "connect"

    }, sort_keys=True, indent=4)
    client.send(sendingData.encode())
    return


def _detect_(client):
    # receivedData 전역변수 사용
    global receivedData
    if (receivedData["status"] == "starting" or receivedData["status"] == "controlling_finished"):
        # detecting 중인 것을 서버에다가 알려야함.
        send_detector_data(client,  status="detecting", classType="resistor",
                           accord_x=0, accord_y=0)
        # 작업 코드 추가하면됩니다....
        print("\n\n\n\n ---- Detecting Elements......---- \n\n\n\n")
        time.sleep(1)
        # 작업 코드 
        # stopping status 시 리턴
        if(receivedData["status"] == "stopping") :
            send_detector_data(client, status="detecting_stopped", classType="resistor",
                           accord_x=30, accord_y=20)
            return; 
        # detecting 끝남 상태 알림
        send_detector_data(client, status="detecting_finished", classType="resistor",
                           accord_x=30, accord_y=20)
    return


def _listener_(client):
    # receivedData 전역변수 사용
    global receivedData
    while True:
        try:
            # dictionary type으로 받기
            tempData = client.recv(1024)
            if not tempData:
                print(tempData)
                raise ConnectionResetError()
            receivedData = json.loads(tempData.decode())
            # print(
            #     f"\n>> [C] received : \n{json.dumps(receivedData,sort_keys=True, indent=4)}")
            print(f">> [Status] {receivedData['status']}")

        except OSError as e:
            print(e)
            print(">> 소켓 서버 연결이 끊긴 것 같습니다. 프로그램을 종료합니다.")
            print(">> input 'quit' to terminate program")
            client.close()
            break
        except json.JSONDecodeError as e:
            print(e)
            print("잘못된 정보를 수신하였습니다.")


def Detector_Client(client):
    # receivedData 전역변수 사용
    global receivedData
    global isDetecting

    isDetecting = bool(False)

    while True:
        if ((not isDetecting)):
            isDetecting = True
            startingDetect = Thread(name="_detect_", target=_detect_,
                                         args=(client,), daemon=True)
            startingDetect.start()
            startingDetect.join()
            isDetecting = False



if (__name__ == "__main__"):
    try:
        # 클라이언트 소켓 생성
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        print('>> Connect Server')
        send_connect_msg(client)
        Listener = Thread(name="_listener_", target=_listener_,
                          args=(client,), daemon=True)
        Listener.start()
        Detector_Client_thread = Thread(name="Detector_Client", target=Detector_Client,
                                        args=(client,), daemon=True)
        Detector_Client_thread.start()

        while True:
            inputData = input('')
            if inputData == 'quit':
                print("exit client")
                break
            elif inputData == 'clear':
                send_detector_data(client, status=receivedData["status"], classType="none",
                                   accord_x=0, accord_y=0)
            elif inputData == 'td':
                send_detector_data(client, status=receivedData["status"], classType="resistor",
                                   accord_x=60, accord_y=60)

    except KeyboardInterrupt as e:
        print('강제종료', e)
    finally:

        client.close()
