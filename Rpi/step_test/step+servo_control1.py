
import time
import RPi.GPIO as GPIO
from collections import deque

#import bus I/O 
import busio
#import SCL/SDA
from board import SCL, SDA
# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

# Set the PWM frequency to 60hz.
pca.frequency = 50

#GPIO STEPMOTOR CONTROL
# GPIO.setmode(GPIO.BOARD)
#2상 바이폴라 스텝모터 모터
AIN1=22 #A #BOARD/BCM 15/22
AIN2=23 #/A #16/23
BIN1=24 #B #18/24
BIN2=25 #/B #22/25
sig=deque([1,1,0,0]) #signal used by deque, rotate
step=200 #default step number
dir=1 #1:forward 0:reverse

cycleTime=0.015 #set cycleTime ->회전속도 조절
intervalTime=cycleTime*4
Freq=intervalTime ** -1

GPIO.setup(AIN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(AIN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BIN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BIN2, GPIO.OUT, initial=GPIO.LOW)

print("주기 : " + str(intervalTime) + "sec")
print("주파수 : " + str(round(Freq,3)) +"Hz")
print("분당회전속도 : " + str(round(1.8/360*Freq*60,3)) +"rpm\n")

def control_base(step) :

    # step=float(input("각도를 입력하세요 : "))
    if step<0 :
        step=step*(-1)
        dir=-1
    else :
        dir=1
    print(step)
    step=int(step/1.8)
    time.sleep(1)
    for i in range(0,step) : #각도조절
        print(sig)
        GPIO.output(AIN1,sig[0])
        GPIO.output(AIN2,sig[2])
        GPIO.output(BIN1,sig[1])
        GPIO.output(BIN2,sig[3])
        time.sleep(cycleTime)
        sig.rotate(dir)
        
    print("1step_end")
    # dir=dir*(-1)
    
    return
# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.
cnt=0x1665
try:
    while True:
        
        # control_base(float(input("각도를 입력하세요 : ")))
        for i in range(0,100) : #각도조절
            print(sig)
            GPIO.output(AIN1,sig[0])
            GPIO.output(AIN2,sig[2])
            GPIO.output(BIN1,sig[1])
            GPIO.output(BIN2,sig[3])
            time.sleep(cycleTime)
            sig.rotate(dir)
        dir=dir*-1
        print("1cycle end")
     
        time.sleep(0.5)
        cnt=0x1565
        
        print("상승")
        while cnt<0x20f0 :
            pca.channels[0].duty_cycle = cnt #10% #channel 0 -> 중간관절
            cnt = cnt + 0x0005
            time.sleep(0.001)
        time.sleep(1)
        
        print("하강")
        while cnt>0x1565 :
            pca.channels[0].duty_cycle = cnt #5% #channel 0 -> 중간관절
            cnt = cnt - 0x0005
            time.sleep(0.001)
        time.sleep(1)
        
        # pca.channels[0].duty_cycle = 0x1665 #5% #channel 0 -> 중간관절
        # time.sleep(1.5)
        # cnt = 0x1465
        print("그리퍼 1")
        pca.channels[1].duty_cycle = 0x1265 #10%
        pca.channels[2].duty_cycle = 0x1afd #10%
        time.sleep(1)
        print("그리퍼 2")
        pca.channels[1].duty_cycle = 0x1fff #5%
        pca.channels[2].duty_cycle = 0x1000 #5%
        time.sleep(1)

        #0x1fff 10% 180 degree
        #0x1265 7.5% 90 degree
        #0x4cc 5% 0 degree

        #pca.channels[0].duty_cycle = 0x1465 #5% #channel 0 -> 중간관절
    
except KeyboardInterrupt:
    pass

GPIO.cleanup()



