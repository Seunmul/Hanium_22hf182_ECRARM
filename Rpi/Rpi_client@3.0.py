from __control__ import Arm

# Import python Internal library
import json
import socket
import time
from threading import Thread

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

# Arm : 매니퓰레이터 클래스 선언
Arm = Arm()

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


def _control_(client, Arm):
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
        print("\n\n>> Controlling Arms .----")
        time.sleep(1)
        # 0. 제어 시간 체크 및 현재 각도 및 각도 제한 범위 표시
        start_time = time.time()
        print(f">> 현재 각도 : {Arm.getCurDegree()}")
        print(">> 각도 제한 범위 : -180<x<180, 0<y<180, -30<z<90 , 0<w<180, 0<r<180 ")
        # 1. 디텍터로부터 수신 데이터 확인 및 데이터 처리(x,y좌표계로 소요 각도 계산)
        print(f">> 디텍터 수신 데이터 : {receivedData['Detector']['data']}")
        # test value
        x_d = 1
        y_d = 1
        z_d = 1
        w_d = 1
        r_d = 1
        s_d = 1
        print(
            f'>> 이동 각도 : "X": {x_d}, "Y": {y_d}, "Z": {z_d}, "W": {w_d}, "R": {r_d}')
        # 2. 각도 계산 데이터를 활용하여 로봇팔 컨트롤 - __CONTROL__ THREAD : X ,Y, Z, W, R
        # 2-1. => 로봇 팔 x,y,z축 제어 => 대략적 위치 조정
        # 2-2. => 로봇 팔 w,r 축 및 그리퍼 제어 => 정밀한 위치 조정
        # 우선은 테스트 데이터만 날림
        X_axis = Thread(name="X_axis", target=Arm._STEP_CONTROL_, args=(
            "X", x_d, Arm.STEPPIN_X, Arm.DIRPIN_X, Arm.ENPIN_X))
        Y_axis = Thread(name="Y_axis", target=Arm._STEP_CONTROL_, args=(
            "Y", y_d, Arm.STEPPIN_Y, Arm.DIRPIN_Y, Arm.ENPIN_Y))
        Z_axis = Thread(name="Z_axis", target=Arm._STEP_CONTROL_, args=(
            "Z", z_d, Arm.STEPPIN_Z, Arm.DIRPIN_Z, Arm.ENPIN_Z))
        W_axis = Thread(name="W_axis", target=Arm._SERVO_CONTROL_, args=(
            "W", w_d, Arm.PCA_CHANNEL_W, Arm.MIN_PWM_W, Arm.INTERVAL_W))
        R_axis = Thread(name="R_axis", target=Arm._SERVO_CONTROL_, args=(
            "R", r_d, Arm.PCA_CHANNEL_R, Arm.MIN_PWM_R, Arm.INTERVAL_R))
        S_axis = Thread(name="S_axis", target=Arm._SERVO_CONTROL_, args=(
            "S", s_d, Arm.PCA_CHANNEL_S, Arm.MIN_PWM_S, Arm.INTERVAL_S))    
        # 배열로 쓰레드 관리
        Axises = [X_axis, Y_axis, Z_axis, W_axis, R_axis, S_axis]
        # start control thread
        for Axis in Axises:
            # print(Axis.name, end=" ")
            Axis.start()
        # wait control thread
        for Axis in Axises:
            Axis.join()
        # update current degree
        Arm.updateCurDegree()  # 내부 degree 업데이트
        # 소요 시간 출력
        print(">> %s seconds ---" % (time.time() - start_time))
        time.sleep(1)
        print(">> Controlling finished")
        print(">> 제어 후  현재 각도 : %s" % (Arm.getCurDegree()))
        print(Arm.getCurDegree()["X"])

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
    global isControlling

    # 컨트롤링 상태 지역변수 선언(컨트롤 중에는 true 상태 유지!)
    isControlling = bool(True)
    print("각도 제한 범위 : -180<theta0<180, 0<theta1<180, -30<theta2<90 , 0<theta3<180, 0<theta4<180, 0<theta5<180 ")
    print("현재 각도 : " + str(Arm.getCurDegree()))
    theta0, theta1, theta2, theta3 , theta4, theta5 = 30, -10, 10, 10, 10, 0
    X_axis = Thread(name="X_axis", target=Arm._STEP_CONTROL_, args=(
        "X", theta0 , Arm.STEPPIN_X, Arm.DIRPIN_X, Arm.ENPIN_X))
    Y_axis = Thread(name="Y_axis", target=Arm._STEP_CONTROL_, args=(
        "Y", theta1, Arm.STEPPIN_Y, Arm.DIRPIN_Y, Arm.ENPIN_Y))
    Z_axis = Thread(name="Z_axis", target=Arm._STEP_CONTROL_, args=(
        "Z", theta2, Arm.STEPPIN_Z, Arm.DIRPIN_Z, Arm.ENPIN_Z))
    W_axis = Thread(name="W_axis", target=Arm._SERVO_CONTROL_, args=(
        "W", theta3, Arm.PCA_CHANNEL_W, Arm.MIN_PWM_W, Arm.INTERVAL_W))
    R_axis = Thread(name="R_axis", target=Arm._SERVO_CONTROL_, args=(
        "R", theta4, Arm.PCA_CHANNEL_R, Arm.MIN_PWM_R, Arm.INTERVAL_R))
    S_axis = Thread(name="S_axis", target=Arm._SERVO_CONTROL_, args=(
        "S", theta5, Arm.PCA_CHANNEL_S, Arm.MIN_PWM_S, Arm.INTERVAL_S))    
    Axises = [X_axis, Y_axis, Z_axis, W_axis, R_axis, S_axis]
    # 중간관절
    Axises[0].start()
    Axises[1].start()
    Axises[2].start()
    Axises[3].start()
    Axises[0].join()
    Axises[1].join()
    Axises[2].join()
    Axises[3].join()
    Arm.updateCurDegree()
    print("현재 각도 : " + str(Arm.getCurDegree()))
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
            isControlling = True
            startingControl = Thread(name="_control_", target=_control_,
                                     args=(client, Arm), daemon=True)
            startingControl.start()
            startingControl.join()
            isControlling = False


if (__name__ == "__main__"):
    try:
        # 로봇팔 초기화
        print("Arm_Control_initializing")
        print(Arm)
        Arm._STEP_SETUP_()
        Arm._SERVO_SETUP_()
        Arm._INIT_()
        
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
        Arm._INIT_()
        print(Arm.getCurDegree())
        print("End")
        client.close()