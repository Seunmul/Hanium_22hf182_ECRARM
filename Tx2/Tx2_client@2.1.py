import json
from threading import Thread
import socket
import time
import sys
import os

#시스템 환경변수로부터 yolov7 path가져오기 : $WORK_HOME - 현재 : /home/seunmul/바탕화면/inference/yolov7
#export WORK_HOME= [yolov7 path로 지정.] 해당  path에 detect_custom.py 있어야함.
sys.path.append(os.environ["WORK_HOME"])
import detect_custom as dc

#주소 불러오기

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

# detector의 데이터를 서버로 전송
def send_detector_data(client, status: str, classType: str,  accord_x: str, accord_y: str):
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
        print("\n\n ---- Detecting Elements......---- \n\n")

        ## 
        # cv2로 이미지 캡쳐 = > 저장 후 image_path를 source로 전달.
        # cap = dc.cv2.VideoCapture(0)
        # if not cap.isOpened():
        #     print("camera open failed")
        #     return
        # ret, img = cap.read()
        # if not ret:
        #     print("Can't read camera")
        #     return
        # img_captured = dc.cv2.imwrite('images/img_captured.jpg', img)
        # cap.release()

        # 모델 인퍼런스 실행.
        # with dc.torch.no_grad():
        #     save_dir,save_path,txt_path = dc.detect_run(dc.device,dc.imgsz,dc.stride,dc.model,dc.half,dc.save_txt,dc.save_img,dc.view_img,source)
        #     print(txt_path,end="\n")
        #     with open(txt_path+".txt", "r") as f:
        #         data=f.read()
        #         print(data)

        #json 파싱. 후 classType, accord_x, accord_y 변수에 저장 , 맨 마지막 라인의 값만!


        # 작업 코드
        # stopping status 시 리턴
        if (receivedData["status"] == "stopping"):
            send_detector_data(client, status="detecting_stopped", classType="resistor",
                               accord_x=receivedData["Detector"]["data"]["x"], accord_y=receivedData["Detector"]["data"]["y"])
            return
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
        time.sleep(0.1)
        if (not isDetecting):
            isDetecting = True
            startingDetect = Thread(name="_detect_", target=_detect_,
                                         args=(client,), daemon=True)
            startingDetect.start()
            startingDetect.join()
            isDetecting = False


if (__name__ == "__main__"):
    try:
        # print(dc)
        # print(dc.opt)
        while True :
            source=input("입력소스 :")
            with dc.torch.no_grad():
                save_dir,save_path,txt_path = dc.detect_run(dc.device,dc.imgsz,dc.stride,dc.model,dc.half,dc.save_txt,dc.save_img,dc.view_img,source)
            print(txt_path,end="\n")
            with open(txt_path+".txt", "r") as f:
                data=f.read()
                print(data)

        # # 클라이언트 소켓 생성
        # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # client.connect((HOST, PORT))
        # print('>> Connect Server')
        # send_connect_msg(client)
        # Listener = Thread(name="_listener_", target=_listener_,
        #                   args=(client,), daemon=True)
        # Listener.start()
        # Detector_Client_thread = Thread(name="Detector_Client", target=Detector_Client,
        #                                 args=(client,), daemon=True)
        # Detector_Client_thread.start()

        # while True:
        #     inputData = input('')
        #     if inputData == 'quit':
        #         print("exit client")
        #         break
        #     elif inputData == 'clear':
        #         send_detector_data(client, status=receivedData["status"], classType="none",
        #                            accord_x=0, accord_y=0)
        #     elif inputData == 'td':
        #         send_detector_data(client, status=receivedData["status"], classType="resistor",
        #                            accord_x=60, accord_y=60)

    except KeyboardInterrupt as e:
        print('강제종료', e)
    finally:

        client.close()
