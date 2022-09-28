#!/bin/bash

export WORK_HOME=$(pwd)/yolov7
echo $WORK_HOME
cp detect_custom.py yolov7/
python Tx2_client@2.2.py
#실행 안되면 python3 명령어로(리눅스,맥 등..)