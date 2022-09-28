#https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

FREQ = 50 #set FREQ
PIN_ARR = [13,15] #testPIN number, 두번째 핀만 사용
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
    time.sleep(1)
    GPIO.setup(PIN_ARR[1],GPIO.IN)

def degree(input):
    print("입력값 " + input)
    if float(input)==0 :
        val=2.4
    elif float(input)>180 :
        val=11.5
    else :
        val=float((11.5-2.4)/180*float(input))+2.4
    return (val)

def SERVO_PWM_CONTROL() :
    
    while True :
        # print(degree(input("각도를 입력하세요(0-180) : ")))
        val = degree(input("각도를 입력하세요(0-180) : "))
        SERVO_PWM_SET(PIN,val)
        print(val)
        print("완료\n")
        # time.sleep(1.4)
        # SERVO_PWM_SET(PIN,2.4)

        # print("0도")
        # time.sleep(1.4)

        
        # SERVO_PWM_SET(PIN,7.1)
            
        # print("90도")
        # time.sleep(1.4)

        
        # SERVO_PWM_SET(PIN,12.05)
            
        # print("180도")
        # time.sleep(1.4)

        
        # SERVO_PWM_SET(PIN,7.1)
            
        # print("90도\n")
        # time.sleep(1.4)
def main():
    try:
        SERVO_PWM_CONTROL()    

    except KeyboardInterrupt:
        print("\nexit GPIO control\n")
        for PIN in PIN_PWM :
            PIN.stop()
        GPIO.cleanup()

def __CONTROL__(data) :

    val = degree(data)
    SERVO_PWM_SET(PIN,val)
    print(val)
    print("완료\n")
    

def __CLEAR_GPIO__() : 
    for PIN in PIN_PWM :
        PIN.stop()
    GPIO.cleanup()

if __name__ == "__main__":
	main()






