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
    "status": "initializing",
    "Detector": {
        "connect": False,
        "data": {
            "class": "none",
            "x": "0",
            "y": "0"
        }
    },
    "Controller": {
        "connect": True,
        "data": {
            "X_Axis": "0",
            "Y_Axis": "0",
            "Z_Axis": "0",
            "R_Axis": "0",
            "W_Axis": "0"
        }
    },
    "Web": {
        "bridgeConnect": False,
        "data": ""
    }
}

# controller의 데이터를 서버로 전송


def send_controller_data(client, status: str, X: str, Y: str, Z: str, W: str, R: str):
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
        "status": "connecting",
        "from": "Controller",
        "data": "connect"

    }, sort_keys=True, indent=4)
    client.send(sendingData.encode())
    return


def _listener_(client):
    # receivedData 전역변수 사용
    global receivedData
    while True:
        try:
            # dictionary type으로 받기
            tempData = client.recv(1024)
            if not tempData:
                raise ConnectionResetError()
            receivedData = json.loads(tempData.decode())
            print(
                f"\n>> [C] received : \n{json.dumps(receivedData,sort_keys=True, indent=4)}")
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


def _control_(client):
    # receivedData 전역변수 사용
    global receivedData
    if (receivedData["status"] == "detecting_finished"):
        # 0. 현재 control status 서버에 알리기
        send_controller_data(client, status="controlling",
                             X=receivedData["Controller"]["data"]["X_Axis"],
                             Y=receivedData["Controller"]["data"]["Y_Axis"],
                             Z=receivedData["Controller"]["data"]["Z_Axis"],
                             W=receivedData["Controller"]["data"]["W_Axis"],
                             R=receivedData["Controller"]["data"]["R_Axis"])
        # 작업 코드 추가하면됩니다....
        print("\n\n ---- Controlling Arms ...---- \n\n")
        # 1. 디텍터로부터 수신 데이터 확인 및 데이터 처리(x,y좌표계로 각도 계산)
        print(f"{receivedData['Detector']['data']}")
        # 2. 각도 계산 데이터를 활용하여
        # 3.

        time.sleep(1)
        # 작업 코드
        ##
        # stopping status 시 리턴
        if (receivedData["status"] == "stopping"):
            send_controller_data(client, status="controlling_stopped",
                                 X=receivedData["Controller"]["data"]["X_Axis"],
                                 Y=receivedData["Controller"]["data"]["Y_Axis"],
                                 Z=receivedData["Controller"]["data"]["Z_Axis"],
                                 W=receivedData["Controller"]["data"]["W_Axis"],
                                 R=receivedData["Controller"]["data"]["R_Axis"])
            return
        # control status 서버에 알리기
        send_controller_data(client, status="controlling_finished",
                             X=int(receivedData["Controller"]
                                   ["data"]["X_Axis"])+1,
                             Y=receivedData["Controller"]["data"]["Y_Axis"],
                             Z=receivedData["Controller"]["data"]["Z_Axis"],
                             W=receivedData["Controller"]["data"]["W_Axis"],
                             R=receivedData["Controller"]["data"]["R_Axis"])
    elif (receivedData["status"] == "manual"):
        # 작업 후
        time.sleep(1)
        # control status 서버에 알리기
        send_controller_data(client, status="manual",
                             X=receivedData["Web"]["data"]["X_Axis"],
                             Y=receivedData["Web"]["data"]["Y_Axis"],
                             Z=receivedData["Web"]["data"]["Z_Axis"],
                             W=receivedData["Web"]["data"]["W_Axis"],
                             R=receivedData["Web"]["data"]["R_Axis"]
                             )
    return


def Controller_Client(client):
    # receivedData 전역변수 사용
    global receivedData
    global isControlling
    # 컨트롤러 초기화 필요

    # 컨트롤링 상태 지역변수 선언(컨트롤 중에는 true 상태 유지!)
    isControlling = bool(False)

    while True:
        time.sleep(0.1)
        if (not isControlling):
            isControlling = True
            startingControl = Thread(name="_control_", target=_control_,
                                     args=(client,), daemon=True)
            startingControl.start()
            startingControl.join()
            isControlling = False


if (__name__ == "__main__"):
    try:
        # 소켓 연결
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        print('>> Connect Server')
        send_connect_msg(client)

        # 메세지 리스너 쓰레드 시작
        Listener = Thread(name="_listener_", target=_listener_,
                          args=(client,), daemon=True)
        Listener.start()

        # 컨트롤러 쓰레드 시작
        Controller_Client_thread = Thread(name="Controller_Client", target=Controller_Client,
                                          args=(client,), daemon=True)
        Controller_Client_thread.start()

        while True:
            inputData = input('')
            if inputData == 'quit':
                print("exit client")
                break
            elif inputData == 'clear':
                send_controller_data(
                    client, status=receivedData["status"], X=0, Y=0, Z=0, W=0, R=0)
            elif inputData == 'td':
                send_controller_data(
                    client, status=receivedData["status"], X=5, Y=5, Z=5, W=5, R=5)

    except KeyboardInterrupt:
        print('강제종료')
    finally:

        client.close()
