<<<<<<< HEAD
# 22_hf182팀 개발코드

---
## 프로젝트 설멍: 딥러닝 기반 객체인식 소자분류로봇 제작
## Platform : Nvidia Jetson Tx2 , RaspberryPi, Python, Tensorflow, YOLOv4 .. etc


=======
# Hanium_22hf182_ECRARM
### 2022한이음 ICT공모전 소자분류로봇 개발 코드 
### Element Classification Robot Arm - Dev Codes
### Contributors : 김영희,박건하,이희원, 차우석 All rights reserved 


개발언어 : python, c/c++, javascript
-----
1. 플레이트에 놓여진 소자를 카메라로 인식한 후 Yolov7기반 커스텀 데이터 모델로 AI 영상처리 및 디텍선 실행
(Inference Device : Jetson Tx2)

2. 디텍션 후 해당 데이터를 로봇팔 컨트롤러가 수신
(Controller : RaspberryPi 4B+)

3. 컨트롤러가 로봇 매니풀레이터 동작 및 분류 알고리즘에 따라 동작 수행

4. 분류함에 소자 분류 완료 시 프로그램 종료.

5. Web Dashboard로 작업상황 확인 가능

BackEnd : python 기반 Socket, WebSocket 라이브러리로 작성. 우선 외부 모델 자체적으로 서버코드 작성,,
추후에 goolge firebase 연동.

FrontEnd : React
>>>>>>> 46a38dd8ede1595ee328b0a0e756af7152ce5646
