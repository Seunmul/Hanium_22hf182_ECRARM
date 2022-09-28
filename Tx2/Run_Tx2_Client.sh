#!/bin/bash

PATH_NAME=$(pwd)
echo $PATH_NAME
PATH_NAME=$PATH_NAME/yolov7
export $PATH_NAME
python3 Tx2_client@2.2.py