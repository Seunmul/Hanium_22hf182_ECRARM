import json
from logging import raiseExceptions
from threading import Thread
import socket
import time

HOST = '155.230.25.98'
# HOST = '127.0.0.1'
PORT = 9999

# recivedData 전역변수 선언
global recivedData
recivedData = {
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
        "status": "connecting",
        "from": "Controller",
        "data": "connect"

    }, sort_keys=True, indent=4)
    client.send(sendingData.encode())
    return


def _control_(client):
    # recivedData 전역변수 사용
    global recivedData
    if (recivedData["status"] == "detecting_finished"):
        # detecting 중인 것을 서버에다가 알려야함.
        send_controller_data(client, status="controlling",
                             X=0, Y=0, Z=0, W=0, R=0)
        # echo 수신 후 동작
        recivedData = json.loads(client.recv(1024).decode())
        print(f"\n>> [D] received : \n{recivedData}")
        # 작업 코드
        print("\n\n\n\n ---- Controlling Arms ...---- \n\n\n\n")
        time.sleep(3)
        # 작업 코드 추가하면됩니다....
        send_controller_data(client, status="controlling_finished",
                             X=10, Y=20, Z=30, W=40, R=50)
    return


def _listener_(client):
    # recivedData 전역변수 사용
    global recivedData
    while True:
        try:
            # dictionary type으로 받기
            tempData = client.recv(1024)
            if not tempData:
                raise ConnectionResetError()
            recivedData = json.loads(tempData.decode())
            print(
                f"\n>> [C] received : \n{json.dumps(recivedData,sort_keys=True, indent=4)}")

        except OSError as e:
            print(e)
            print(">> 소켓 서버 연결이 끊긴 것 같습니다. 프로그램을 종료합니다.")
            print(">> input 'quit' to terminate program")
            client.close()
            break
        except json.JSONDecodeError as e:
            print(e)
            print("잘못된 정보를 수신하였습니다.")


def Controller_Client(client):
    # recivedData 전역변수 사용
    global recivedData
    global isControlling

    isControlling = bool(False)
    
    while True:
        if ((not isControlling) and recivedData["status"] == "detecting_finished"):
            isControlling = True
            send_controller_data(client, status="controlling",
                                 X=0, Y=0, Z=0, W=0, R=0)
            # 작업 코드
            print("\n\n\n\n ---- Controlling Arms ...---- \n\n\n\n")
            time.sleep(3)
            # 작업 코드 추가하면됩니다....
            send_controller_data(client, status="controlling_finished",
                                 X=10, Y=20, Z=30, W=40, R=50)
            isControlling = False
        elif (recivedData["status"] == "stopping"):
            isControlling = False
        else :
            pass

    # if (isControlling) :
    #     startingControl = Thread(name="_control_", target=_control_,
    #                                  args=(client,), daemon=True)
    #     startingControl.start()
    #     startingControl.join()

    # while True:
    #     else:
    #         print(f"\n>> [C] received : \n{recivedData}")
    #         if (recivedData["status"] == "stopping"):
    #             print("stopping...")
    #             print("stopped")
    #             send_controller_data(client, status="stopping",
    #                      X=0, Y=0, Z=0, W=0, R=0)
    #         startingControl = Thread(name="_control_", target=_control_,
    #                                      args=(client,), daemon=True)
    #         startingControl.start()
    #         startingControl.join()
    #     finally:
    #         pass


if (__name__ == "__main__"):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        print('>> Connect Server')
        send_connect_msg(client)
        Listener = Thread(name="_listener_", target=_listener_,
                      args=(client,), daemon=True)
        Listener.start()
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
                    client, status=recivedData["status"], X=0, Y=0, Z=0, W=0, R=0)
            elif inputData == 'td':
                send_controller_data(
                    client, status=recivedData["status"], X=5, Y=5, Z=5, W=5, R=5)

    except KeyboardInterrupt:
        print('강제종료')
    finally:

        client.close()
