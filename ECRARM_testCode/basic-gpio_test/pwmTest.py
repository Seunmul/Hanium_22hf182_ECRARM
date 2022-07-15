#https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
##pwm Servo motor control 테스트 코드
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD) #보드 핀 배열 사용

FREQ = 50 #set FREQ
PIN_ARR = [13,15] #testPIN number
PIN_PWM = []

for PIN in PIN_ARR :
    GPIO.setup(PIN,GPIO.OUT) #GPIO PIN number에 맞게 셋업 : GPIO.OUT / GPIO.IN   
    PIN = GPIO.PWM(PIN,FREQ) #p=GPIO.PWM(channel, freq)
    PIN.start(0) #p.start(dc) where dc is duty cycle
    PIN_PWM.append(PIN)

print(PIN_PWM)
delay = 0.1

def testLED_PWM() :
    while True :
            for i in range(0, FREQ):
                for PIN in PIN_PWM :
                    PIN.ChangeDutyCycle(i)
                time.sleep(delay)
            for i in range(FREQ,-1,-1):
                for PIN in PIN_PWM :
                    PIN.ChangeDutyCycle(i)
                time.sleep(delay)

def SERVO_PWM_SET(PIN,dutyCycle):
    GPIO.setup(PIN_ARR[1],GPIO.OUT) #GPIO PIN number에 맞게 셋업 : GPIO.OUT / GPIO.IN   
    PIN_PWM[1].ChangeDutyCycle(dutyCycle)
    time.sleep(0.6)
    GPIO.setup(PIN_ARR[1],GPIO.IN) # GPIO 사용 후 OUT --> IN 추가적인 떨림 제거

def SERVO_PWM_CONTROL() :
    
    while True :
        
        SERVO_PWM_SET(PIN,2.4)

        print("0도")
        time.sleep(1.4)

        
        SERVO_PWM_SET(PIN,7.1)
            
        print("90도")
        time.sleep(1.4)

        
        SERVO_PWM_SET(PIN,12.05)
            
        print("180도")
        time.sleep(1.4)

        
        SERVO_PWM_SET(PIN,7.1)
            
        print("90도\n")
        time.sleep(1.4)
    
try:
    SERVO_PWM_CONTROL()    

except KeyboardInterrupt:
    print("\nexit GPIO control\n")
    for PIN in PIN_PWM :
        PIN.stop()
    GPIO.cleanup()





