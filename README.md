
=======
# Hanium_22hf182_ECRARM
### 2022한이음 ICT공모전 소자분류로봇 개발 코드 
### Element Classification Robot Arm - Dev Codes
### Contributors : 김영희,박건하,이희원, 차우석 All rights reserved 
---
### 프로젝트 설멍: 딥러닝 기반 객체인식 소자분류로봇 제작
### Platform : Nvidia Jetson Tx2 , RaspberryPi,
### last update 0915

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


----
#### 가상환경 설정 방법
venv 사용하는데,
테스트용도로만 사용하시고 torch, torchvision, opencv 등은 직접 빌드하시는 걸 추천드립니다.

python -m venv ECRARM_PY_ENV
source ECRARM_PY_ENV/Scripts/activate
pip install -r requirements.txt

하고 실행하시면 됩니다.

가상환경 해제 시 터미널에 deactivate

venv관련해서 찾아보시고 사용해주세요. 
로컬에서 사용하셔도 상관 없습니다.