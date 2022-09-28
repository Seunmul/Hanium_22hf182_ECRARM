# Tx2 업로드 코드
----
Jetson Tx2 혹은 인퍼런스용 디바이스 필요.
python 3.7 이상 필요.

## Tx2_client.py 
tx2보드 소켓 클라이언트 코드
### Tx2_client@1.1py
- yolov7 인퍼런스 코드 미포함

[version]>2
### Tx2_client@[version].py
- yolov7 인퍼런스 코드 포함
- WORK_HOME 환경변수 설정 및 해당 path에 yolov7모델 있어야 함.
- yolov7 커스텀 가중치 파일이 Tx2_client@[version].py와 같은 곳에 위치해야함.(현재 폴더 위치)
- git clone https://github.com/WongKinYiu/yolov7.git
- yolov7 디렉토리가 Tx2/yolov7에 위치해야함.

### detect_custom.py
- yolov7 디렉토리 내에 위치해야함. Tx2_client@[version]>2.1에서 해당 파일을 불러옴.

----
처음 셋팅 방법
venv나, pipenv 또는 아나콘다 가상환경 사용을 권장드립니다.
가상환경 활성화 후
pip install -r requirements.txt 하면 패키지 깔리고

이후에 Tx2_run_client.sh 쉘 실행시켜먼 됩니다.
쉘 스크립트 실행 시 

1. yolov7 폴더가 없으면 자동으로 깃허브에서 깔리고
있다면 그냥 Tx2_client@2.2.py 실행됩니다.

혹시라도 Tx2_client@2.2.py 파일의 이름을 변경하셨다면 쉘 스크립트 이름도 같이 수정해주시기 바립니다.

2. 디렉토리에 있는 detect_custom.py가 yolov7폴더로 복사되니 
추가적인 수정이 필요하시면 detect_custom.py를 수정하시면 됩니다.

추후에 yolov7패치에 따라서 대응하셔야 합니다.

