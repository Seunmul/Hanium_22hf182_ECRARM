#-*- coding: utf-8 -*-
import json
from threading import Thread
import socket
import time
import sys
import os

# 시스템 환경변수로부터 yolov7 path가져오기 : $WORK_HOME
print(">> LOADING ML DETECITON MODEL ")
sys.path.append(os.environ["WORK_HOME"])
import detect_custom as dc

# 전역변수 선언
global FRAME, capture, w_min, w_max, h_min, h_max

# 카메라 로드 -> FRAME 전역변수에 계속 저장.
def Load_Camera(index: int):
    global FRAME, capture, w_min, w_max, h_min, h_max

    print(">> 카메라 로드 중...")

    # VideoCapture : 카메라 열기
    capture = dc.cv2.VideoCapture(index)
    print(type(capture))
    print(capture)
    
    # 원본 동영상 크기 정보
    w = capture.get(dc.cv2.CAP_PROP_FRAME_WIDTH)
    h = capture.get(dc.cv2.CAP_PROP_FRAME_HEIGHT)
    print(">> 원본 동영상 너비(가로) : {}, 높이(세로) : {}".format(w, h))

    # 동영상 크기 변환
    #capture.set(dc.cv2.CAP_PROP_FRAME_WIDTH, 1920)  # 가로
    #capture.set(dc.cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # 세로
    capture.set(dc.cv2.CAP_PROP_FRAME_WIDTH, 1280)  # 가로
    capture.set(dc.cv2.CAP_PROP_FRAME_HEIGHT, 720)  # 세로
    # 변환된 동영상 크기 정보
    w = capture.get(dc.cv2.CAP_PROP_FRAME_WIDTH)
    h = capture.get(dc.cv2.CAP_PROP_FRAME_HEIGHT)

    print(">> 변환된 동영상 너비(가로) : {}, 높이(세로) : {}".format(w, h))
    
    w_min =int(w*0.25)#320
    w_max =int(w*0.75)#960
    h_min =int(h*0.07)#50
    h_max =int(h*0.93)#670
    print(f'{w_min} X {w_max} | {h_min} X {h_max} ')
    
    print(">> 카메라 로드 완료.")


    while True:
        retval, FRAME = capture.read()
        
        # 읽은 프레임이 없는 경우 종료
        if not retval:
            break

    # 카메라 메모리 연결 해제
    capture.release()
    print(">> release memory")
    return

if (__name__ == "__main__"):
    try:
        # 카메라 인덱스
        camera_index = 1 
        
        # 카메라 연결
        camera_listener = Thread(name="Load_Camera", target=Load_Camera,
                                 args=(camera_index,), daemon=True)
        camera_listener.start()
        time.sleep(3)
        while True:
            inputData = input('y or quit : ')

            if inputData == 'quit':
                print("exit client")
                break

            elif inputData == 'y':
                # 모델 인퍼런스 실행.
                print(f" >> get img data from mem : {type(FRAME)}",end="\n\n")
                # print(FRAME)
                print(type(FRAME))
                print(FRAME.shape)
                #img=FRAME[75:1004,480:1440].copy()
                img=FRAME[50:670,320:960].copy() 
                with dc.torch.no_grad():
                    save_dir, save_path, txt_path = dc.detect_run(
                        dc.device, dc.imgsz, dc.stride, dc.model, dc.half, dc.save_txt, dc.save_img, dc.view_img, img)
                print(txt_path, end="\n\n")

    except KeyboardInterrupt as e:
        print('강제종료', e)
    finally:
        capture.release()
        # 모든 창 닫기
        print('test finishied')
