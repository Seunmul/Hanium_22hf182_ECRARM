#스텝모터 제어 예시 코드 1
import RPi.GPIO as GPIO
from time import sleep
from collections import deque

GPIO.setmode(GPIO.BOARD)#2상 바이폴라 스텝모터 모터
AIN1=15 #A
AIN2=16 #/A
BIN1=18 #B
BIN2=22 #/B
sig=deque([1,1,0,0]) #signal used by deque, rotate
step=200 #default step number
dir=1 # 1:forward 0:reverse

cycleTime=0.015 #set cycleTime ->회전속도 조절
intervalTime=cycleTime*4
Freq=1/intervalTime

GPIO.setup(AIN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(AIN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BIN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BIN2, GPIO.OUT, initial=GPIO.LOW)

print("주기 : " + intervalTime + "sec")
print("주파수 : " + intervalTime +"Hz")

try:
    while 1:
        step=float(input("각도를 입력하세요 : "))
        if step<0 :
            step=step*(-1)
            dir=-1
        else :
            dir=1
        print(step)
        step=int(step/1.8)
        sleep(1)
        for i in range(0,step) : #각도조절
            print(sig)
            GPIO.output(AIN1,sig[0])
            GPIO.output(AIN2,sig[2])
            GPIO.output(BIN1,sig[1])
            GPIO.output(BIN2,sig[3])
            sleep(cycleTime)
            sig.rotate(dir)
            
        print("1step_end")
        # dir=dir*(-1)
        sleep(0.5)
except KeyboardInterrupt:
    pass

GPIO.cleanup()


