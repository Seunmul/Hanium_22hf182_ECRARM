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

