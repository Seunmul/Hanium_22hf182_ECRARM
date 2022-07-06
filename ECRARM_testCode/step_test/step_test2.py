#-*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
StepPins = [15,16,18,22]

#핀 출력 설정

for pin in StepPins:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin,False)

StepCounter = 0 #스텝 수 세는 변수

# 싱글 코일 여자 방식 시퀀스

StepCount = 4

Seq = [[0,0,0,1],
       [0,0,1,0],
       [0,1,0,0],
       [1,0,0,0]]

try:
    while 1: #무한 반복
        for pin in range(0, 4):
            xpin = StepPins[pin]
            if Seq[StepCounter][pin]!=0: #Seq[][]가 0이 아니면 동작
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)

        StepCounter += 1 #1 증가

        # 시퀀스가 끝나면 다시 시작

        if (StepCounter==StepCount):
            StepCounter = 0
        if (StepCounter<0):
            StepCounter = StepCount

        #다음 동작 기다리기
        time.sleep(1)
except KeyboardInterrupt: #Ctrl+c => 종료
    GPIO.cleanup()
 