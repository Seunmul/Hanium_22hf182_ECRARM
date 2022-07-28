#https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

FREQ = 50 #set FREQ
PIN_ARR = [13,15] #testPIN number
PIN_PWM = []

for PIN in PIN_ARR :
    GPIO.setup(PIN,GPIO.OUT) #GPIO PIN number에 맞게 셋업 : GPIO.OUT / GPIO.IN   
    PIN = GPIO.PWM(PIN,FREQ) #p=GPIO.PWM(channel, freq)
    PIN.start(2.4) #p.start(dc) where dc is duty cycle
    PIN_PWM.append(PIN)

print(PIN_PWM)
delay = 0.1

def degree(input):
    print("입력값 " + input)
    if float(input)==0 :
        val=2.4
    elif float(input)>180 :
        val=11.5
    else :
        val=float((11.5-2.4)/180*float(input))+2.4
    return (val)


def SERVO_PWM_SET(PIN,dutyCycle):
    
    PIN_PWM[1].ChangeDutyCycle(dutyCycle)
    time.sleep(0.01)
    
    # GPIO.setup(PIN_ARR[1],GPIO.IN)

def SERVO_PWM_CONTROL() :
    val = 3.4
    init = 6
    while init>val :
        init = init - 0.1
        SERVO_PWM_SET(PIN,init)
        time.sleep(0.01)
        print("init>val")
        print(init)
    print("초기화중...")
    SERVO_PWM_SET(PIN,val)
    init = val
    print(init)
    time.sleep(0.01)
    # GPIO.setup(PIN_ARR[1],GPIO.IN)
    print("완료")

    while True :
        GPIO.setup(PIN_ARR[1],GPIO.OUT) #GPIO PIN number에 맞게 셋업 : GPIO.OUT / GPIO.IN   
        val = degree(input("각도를 입력하세요(0-180) : "))
        
        if(init>val) :
            while init>val :
                init = init - 0.08
                SERVO_PWM_SET(PIN,init)
                print("init>val")
                print(init)
                time.sleep(0.01)

        elif(init<val) :
            while init<val :
                init = init + 0.08
                SERVO_PWM_SET(PIN,init)
                print("init<val")
                print(init)
                time.sleep(0.01)

        SERVO_PWM_SET(PIN,val)
        


        print(val)
        print("완료\n")

        init = val
        
        GPIO.setup(PIN_ARR[1],GPIO.IN)
        time.sleep(0.1)
        # SERVO_PWM_SET(PIN,7.1)
            
        # print("90도")
        # time.sleep(1.4)

        
        # SERVO_PWM_SET(PIN,12.05)
            
        # print("180도")
        # time.sleep(1.4)

        
        # SERVO_PWM_SET(PIN,7.1)
            
        # print("90도\n")
        # time.sleep(1.4)
    
try:
    SERVO_PWM_CONTROL()    

except KeyboardInterrupt:
    print("\nexit GPIO control\n")
    for PIN in PIN_PWM :
        PIN.stop()
    GPIO.cleanup()





