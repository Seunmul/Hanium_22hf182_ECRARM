from __control__ import GPIO
from __control__ import Arm
from __calculation__ import CALCUL

# Import python Internal library
import json
import socket
import time
from threading import Thread

# element class
# 0: IC chip
# 1: LED
# 2: capacitor
# 3: resistor
# 4: transistor

# HOST = '155.230.25.98'
# HOST = '127.0.0.1'
HOST = '192.168.0.15'
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

# Arm : 매니퓰레이터 클래스 선언
Arm = Arm()
# CALCUL : 계산 클래스 선언
CALCUL = CALCUL()

# connect 메시지 전송 및 이니셜라이즈
def send_connect_msg(client):
    sendingData = json.dumps({
        "status": "connecting",
        "from": "Controller",
        "data": "connect"

    }, sort_keys=True, indent=4)
    client.send(sendingData.encode())

    return

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

# 서버 메세지 리스너
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


# arm control
def _arm_control_(client,Arm, x_d, y_d, z_d, w_d, r_d, s_d):
    # 0. 제어 시간 체크
    start_time = time.time()
    print("현재 각도 : " + str(Arm.getCurDegree()))
    X_axis = Thread(name="X_axis", target=Arm._STEP_CONTROL_, args=(
        "X", x_d, Arm.STEPPIN_X, Arm.DIRPIN_X, Arm.ENPIN_X,), daemon=True)
    Y_axis = Thread(name="Y_axis", target=Arm._STEP_CONTROL_, args=(
        "Y", y_d, Arm.STEPPIN_Y, Arm.DIRPIN_Y, Arm.ENPIN_Y,), daemon=True)
    Z_axis = Thread(name="Z_axis", target=Arm._STEP_CONTROL_, args=(
        "Z", z_d, Arm.STEPPIN_Z, Arm.DIRPIN_Z, Arm.ENPIN_Z,), daemon=True)
    W_axis = Thread(name="W_axis", target=Arm._SERVO_CONTROL_, args=(
        "W", w_d, Arm.PCA_CHANNEL_W, Arm.MIN_PWM_W, Arm.INTERVAL_W,), daemon=True)
    R_axis = Thread(name="R_axis", target=Arm._SERVO_CONTROL_, args=(
        "R", r_d, Arm.PCA_CHANNEL_R, Arm.MIN_PWM_R, Arm.INTERVAL_R,), daemon=True)
    S_axis = Thread(name="S_axis", target=Arm._SERVO_CONTROL_, args=(
        "S", s_d, Arm.PCA_CHANNEL_S, Arm.MIN_PWM_S, Arm.INTERVAL_S,), daemon=True)

    Axises = [X_axis, Y_axis, Z_axis, W_axis, R_axis, S_axis]

    # start control thread
    for Axis in Axises:
        # print(Axis.name, end=" ")
        Axis.start()
    # wait control thread
    for Axis in Axises:
        Axis.join()

    # 소요 시간 및 현재 각도 출력
    print(f">> {time.time() - start_time} seconds")
    print(f">> 현재 각도 : {Arm.getCurDegree()}")
    Arm.updateCurDegree()

    # 서버로 현재각도 전송.
    send_controller_data(client, status="controlling",
                                X=str(Arm.getCurDegree()["X"]),
                                Y=str(Arm.getCurDegree()["Y"]),
                                Z=str(Arm.getCurDegree()["Z"]),
                                W=str(Arm.getCurDegree()["W"]),
                                R=str(Arm.getCurDegree()["R"]))
    return

# 컨트롤
def _control_(client, Arm):
    # receivedData 전역변수 사용
    global receivedData
    if (receivedData["status"] == "detecting_finished"):
        # 현재 control status 서버에 알리기
        send_controller_data(client, status="controlling",
                                 X=str(Arm.getCurDegree()["X"]),
                                 Y=str(Arm.getCurDegree()["Y"]),
                                 Z=str(Arm.getCurDegree()["Z"]),
                                 W=str(Arm.getCurDegree()["W"]),
                                 R=str(Arm.getCurDegree()["R"]))

        # 작업 코드 추가하면됩니다....
        print("\n\n>> Controlling Arms .----")
        
        # print(">> 각도 제한 범위 : -180<x<180, 0<y<170, -30<z<90 , 0<w<180, 0<r<180 ")

        # 1. 디텍터로부터 수신 데이터 확인 및 데이터 처리(x,y좌표계로 소요 각도 계산)
        # x 축 제어
        x_d, y_d, z_d, w_d, r_d, s_d = 0, 0, 0, 0, 0, 0
        x = float(receivedData['Detector']['data']['x'])*9
        y = 8 - float(receivedData['Detector']['data']['x'])*16

        R, x_d = CALCUL.changeCoordinate(y,x)
        _arm_control_(client,Arm, x_d=x_d, y_d=0, z_d=0, w_d=0, r_d=0, s_d=0)

        # 라이다로 거리 줄이는 코드
        height = CALCUL.HEIGHT
        # while(1) :
        #     time.sleep(0.1)
        #     y_d, z_d, w_d = CALCUL.calculAngle(R, height)
        #     y_d = y_d - Arm.degree.get('Y')
        #     z_d = z_d - Arm.degree.get('Z')
        #     w_d = w_d - Arm.degree.get('W')   
            
        #     _arm_control_(client,Arm, x_d=0, y_d=y_d, z_d=z_d, w_d=w_d, r_d=0, s_d=0)

        #     if CALCUL.CHECK_DIS > CALCUL.detect_distance() : 
        #         Arm.getElement()
        #         break
        #     else :
        #         height = CALCUL.decreaseDis(height)

        # y축만 초기상태로
        y_d = 90 - Arm.degree.get('W')
        _arm_control_(client,Arm, x_d=0, y_d=y_d, z_d=0, w_d=0, r_d=0, s_d=0)           
        
        # 분류통으로 이동
        print(f">> 디텍터 수신 데이터 : {receivedData['Detector']['data']}")
        if(int(receivedData['Detector']['data']['class']) == 0):
            print(">>IC CHIP")
            x_d = Arm.sort_buckets[0][0] - Arm.degree.get("X")
            y_d = Arm.sort_buckets[0][1] - Arm.degree.get("Y")  
            z_d = Arm.sort_buckets[0][2] - Arm.degree.get("Z")  
            w_d = Arm.sort_buckets[0][3] - Arm.degree.get("W") 
        elif(int(receivedData['Detector']['data']['class']) == 1):
            print(">>LED")
            x_d = Arm.sort_buckets[1][0] - Arm.degree.get("X")
            y_d = Arm.sort_buckets[1][1] - Arm.degree.get("Y")  
            z_d = Arm.sort_buckets[1][2] - Arm.degree.get("Z")  
            w_d = Arm.sort_buckets[1][3] - Arm.degree.get("W")
        elif(int(receivedData['Detector']['data']['class']) == 2):
            print(">>Capacitor")
            x_d = Arm.sort_buckets[2][0] - Arm.degree.get("X")
            y_d = Arm.sort_buckets[2][1] - Arm.degree.get("Y")  
            z_d = Arm.sort_buckets[2][2] - Arm.degree.get("Z")  
            w_d = Arm.sort_buckets[2][3] - Arm.degree.get("W")
        elif(int(receivedData['Detector']['data']['class']) == 3):
            print(">>Resistor")
            x_d = Arm.sort_buckets[3][0] - Arm.degree.get("X")
            y_d = Arm.sort_buckets[3][1] - Arm.degree.get("Y")  
            z_d = Arm.sort_buckets[3][2] - Arm.degree.get("Z")  
            w_d = Arm.sort_buckets[3][3] - Arm.degree.get("W")
        elif(int(receivedData['Detector']['data']['class']) == 4):
            print(">>Transistor")
            x_d = Arm.sort_buckets[4][0] - Arm.degree.get("X")
            y_d = Arm.sort_buckets[4][1] - Arm.degree.get("Y")  
            z_d = Arm.sort_buckets[4][2] - Arm.degree.get("Z")  
            w_d = Arm.sort_buckets[4][3] - Arm.degree.get("W")        # test value

        _arm_control_(client,Arm, x_d=x_d, y_d=y_d, z_d=z_d, w_d=w_d, r_d=r_d, s_d=s_d)
        
        # 소자 놓기 및 초기상태
        time.sleep(0.5)
        Arm.releaseElement()
        Arm._INIT_()

        print(">> Controlling finished")
        print(">> 제어 후  현재 각도 : %s" % (Arm.getCurDegree()))

        ##### 실행 중 stopping status 시 리턴,  나중에 curDegree값을 전송해주면 됨. #####
        if (receivedData["status"] == "stopping"):
            send_controller_data(client, status="controlling_stopped",
                                 X=str(Arm.getCurDegree()["X"]),
                                 Y=str(Arm.getCurDegree()["Y"]),
                                 Z=str(Arm.getCurDegree()["Z"]),
                                 W=str(Arm.getCurDegree()["W"]),
                                 R=str(Arm.getCurDegree()["R"]))
            return

        # 3. control-finished status 서버에 알리기, 나중에 curDegree값을 전송해주면 됨.
        send_controller_data(client, status="controlling_finished",
                             X=str(Arm.getCurDegree()["X"]),
                             Y=str(Arm.getCurDegree()["Y"]),
                             Z=str(Arm.getCurDegree()["Z"]),
                             W=str(Arm.getCurDegree()["W"]),
                             R=str(Arm.getCurDegree()["R"]))
    # elif (receivedData["status"] == "manual"):
    #     # 작업 후
    #     time.sleep(1)
    #     # control status 서버에 알리기
    #     send_controller_data(client, status="manual",
    #                          X=receivedData["Web"]["data"]["X_Axis"],
    #                          Y=receivedData["Web"]["data"]["Y_Axis"],
    #                          Z=receivedData["Web"]["data"]["Z_Axis"],
    #                          W=receivedData["Web"]["data"]["W_Axis"],
    #                          R=receivedData["Web"]["data"]["R_Axis"]
    #                          )
    return


def Controller_Client(client, Arm):
    # receivedData 전역변수 사용
    global receivedData

    # 컨트롤링 상태 지역변수 선언(컨트롤 중에는 true 상태 유지!)
    isControlling = bool(False)

    # 초기 상태 전송
    send_controller_data(client, status="initializing",
                         X=str(Arm.getCurDegree()["X"]),
                         Y=str(Arm.getCurDegree()["Y"]),
                         Z=str(Arm.getCurDegree()["Z"]),
                         W=str(Arm.getCurDegree()["W"]),
                         R=str(Arm.getCurDegree()["R"]))
    print(">> sending initial state degree...")

    while True:
        time.sleep(0.1)
        if (not isControlling):
            isControlling = bool(True)
            startingControl = Thread(name="_control_", target=_control_,
                                     args=(client, Arm,), daemon=True)
            startingControl.start()
            startingControl.join()
            isControlling = bool(False)


if (__name__ == "__main__"):
    try:
        # 로봇팔 초기화
        print("Arm_Control_initializing")
        print(Arm)
        GPIO.cleanup()
        Arm._STEP_SETUP_()
        Arm._SERVO_SETUP_()
        Arm._INIT_()
        Arm.setElectromagnetic()
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
                                          args=(client, Arm,), daemon=True)
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
        # 종료 시 로봇팔 초기화
        print("\n\nback to initialize state...")
        Arm._FIN_()
        print("PINS OFF")
        Arm._STEP_OFF_()
        print(Arm.getCurDegree())
        print("End")
        client.close()
