import json
from threading import Thread
import socket
import time
import sys
import os

print(">> LOADING ML DETECITON MODEL ")
#시스템 환경변수로부터 yolov7 path가져오기 : $WORK_HOME
sys.path.append(os.environ["WORK_HOME"])
import detect_custom as dc

#소켓 서버 주소 불러오기

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
global detectedData
detectedData={
    "class":"none",
    "x":"none",
    "y":"none"
}

# detector의 데이터를 서버로 전송
def send_detector_data(client, status: str, classType: str,  x: str, y: str):
    sendingData = json.dumps({
        "status": status,
        "from": "Detector",
        "data": {
                "class": classType,
                "x": str(x),
                "y": str(y)
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
    global detectedData
    if (receivedData["status"] == "starting" or receivedData["status"] == "controlling_finished"):
        # detecting 중인 것을 서버에다가 알려야함.
        send_detector_data(client,  status="detecting", classType="detecting",
                           x="detecting", y="detecting")
        time.sleep(0.1)
        # 작업 코드 추가하면됩니다....
        print("\n\n ---- Detecting Elements......---- \n\n")
        try :
            # cv2로 이미지 캡쳐 = > 저장 후 image_path를 source로 전달.
            cap = dc.cv2.VideoCapture(0)
            if not cap.isOpened():
               print("camera open failed")
               raise RuntimeError
            ret, img = cap.read()
            if not ret:
               print("Can't read camera")
               raise RuntimeError

            crop_img = img[120:-120,160:-160]
            scaleX = 2
            scaleY = 2
            scaleUp_img = dc.cv2.resize(crop_img, None, fx=scaleX, fy=scaleY, interpolation = dc.cv2.INTER_CUBIC)

            img_captured = dc.cv2.imwrite('images/img_captured.jpg', scaleUp_img)

            cap.release()
            # 모델 인퍼런스 실행.
            # source="images/bus.jpg"
            source="images/img_captured.jpg"
            with dc.torch.no_grad():
                save_dir,save_path,txt_path = dc.detect_run(dc.device,dc.imgsz,dc.stride,dc.model,dc.half,dc.save_txt,dc.save_img,dc.view_img,source)
            print(txt_path,end="\n")
            #txt파일 불러와서 detectedData 변수에 저장 #형식 : {'class': '5', 'x': '0.501852', 'y': '0.446759', 'm': '0.979012', 'h': '0.465741'}
            with open(txt_path+".txt", "r") as f:
                lines = f.read().splitlines()
                key=lines[0].split()
                data=lines[-1].split()
                for i in range(0,len(key)):
                    detectedData[key[i]]=data[i]
                print(detectedData)
        except FileNotFoundError as e:
            # time.sleep(2)
            print("\n아무것도 인식되지 않았습니다. 프로그램을 종료합니다. \n")
            send_detector_data(client, status="initializing", classType="FINISHED",
                                   x="FINISHED", y="FINISHED")
        except Exception as e:
            time.sleep(3)
            #에러 발생 시
            print(e)
            print(">> Error ocuured during detecting.")
            send_detector_data(client, status="stopping", classType="ERROR",
                                   x="ERROR", y="ERROR")
        else :
            #json 파싱. 후 classType, x, y 변수에 저장 , 맨 마지막 라인의 값만!
            # time.sleep(1) # 인퍼런스 너무 빨라서 넣어놓음;;;

            # 작업 코드
            # stopping status 시 리턴
            if (receivedData["status"] == "stopping"):
                send_detector_data(client, status="detecting_stopped", classType=detectedData["class"],
                                   x=detectedData["x"], y=detectedData["y"])
                return
            # detecting 끝남 상태 알림
            send_detector_data(client, status="detecting_finished", classType=detectedData["class"],
                                   x=detectedData["x"], y=detectedData["y"])
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
                                   x=0, y=0)
            elif inputData == 'td':
                send_detector_data(client, status=receivedData["status"], classType="resistor",
                                   x=60, y=60)

    except KeyboardInterrupt as e:
        print('강제종료', e)
    finally:

        client.close()
