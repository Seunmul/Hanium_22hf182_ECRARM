#!/bin/bash

export WORK_HOME=$(pwd)/yolov7

# yolov7 폴더 없으면 git clone https://github.com/WongKinYiu/yolov7.git yolov7 실행
if [ ! -d ./yolov7 ]; then
    echo NO yolov7 directory;
    echo cloning yolov7 repository......;
    git clone https://github.com/WongKinYiu/yolov7.git yolov7
fi

echo $WORK_HOME
cp detect_custom.py yolov7/
python Tx2_client@3.0.py
#실행 안되면 python3 명령어로(리눅스,맥 등..)