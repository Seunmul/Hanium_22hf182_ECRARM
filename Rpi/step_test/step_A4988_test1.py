#import libraries
import RPi.GPIO as GPIO
import time

def __SETUP__(PINS,FREQ=60):

    #set GPIO mode => BOARD, BOARD GPIO = physical GPIO
    GPIO.setmode(GPIO.BOARD)
    #set Pins number
    PINS = PINS
    #set FREQ
    FREQ = FREQ

    #setup GPIO PINS
    for PIN in PINS :
        print(PIN)
        GPIO.setup(PIN,GPIO.OUT) #GPIO PIN number에 맞게 셋업 : GPIO.OUT / GPIO.IN   

def __CONTORL__(STEP,STEPPIN,DIRPIN,ENPIN):
    
    STEP=int(STEP)
    GPIO.output(ENPIN,GPIO.LOW); # set ENPIN LOW => start control
    try :
        #clockwise
        GPIO.output(DIRPIN,GPIO.HIGH)
        print("clockwise")
        for i in range(0,STEP) :
            GPIO.output(STEPPIN,GPIO.LOW)
            time.sleep(0.0001)
            GPIO.output(STEPPIN,GPIO.HIGH)
            time.sleep(0.0001) 
            # print(i)
        time.sleep(1)
        GPIO.output(ENPIN,GPIO.HIGH) # set ENPIN HIGH
    except KeyboardInterrupt :
        pass
    GPIO.output(ENPIN,GPIO.HIGH) # set ENPIN HIGH
    return 
    
if __name__ =="__main__":
    print("step+A4988_test1.py")
    #control params
    STEPPIN = 29
    DIRPIN = 31
    ENPIN = 33
    STPES_PER_REVOLUTION = 1600
    FREQ= 60
    PINS = [STEPPIN,DIRPIN,ENPIN,35]

    __SETUP__(PINS,FREQ)
    GPIO.output(ENPIN,GPIO.LOW); # set ENPIN LOW => start control
    try :
        while True:
            #clockwise
            GPIO.output(DIRPIN,GPIO.HIGH)
            print("clockwise")
            for i in range(0,STPES_PER_REVOLUTION) :
                GPIO.output(STEPPIN,GPIO.LOW)
                time.sleep(0.0001)
                GPIO.output(STEPPIN,GPIO.HIGH)
                time.sleep(0.0001) 
                # print(i)
            GPIO.output(ENPIN,GPIO.HIGH) # set ENPIN HIGH
            time.sleep(1.5)
            GPIO.output(ENPIN,GPIO.LOW) # set ENPIN LOW => start control
            
            #counterclockwise
            GPIO.output(DIRPIN,GPIO.LOW) # set ENPIN LOW => start control
            print("counterclockwise")
            for i in range(0,STPES_PER_REVOLUTION) :
                GPIO.output(STEPPIN,GPIO.LOW)
                time.sleep(0.0001)
                GPIO.output(STEPPIN,GPIO.HIGH)
                time.sleep(0.0001)
            
            #stop
            print("stop\n")
            GPIO.output(ENPIN,GPIO.HIGH) # set ENPIN HIGH
            time.sleep(1.5)

            #restart
            GPIO.output(ENPIN,GPIO.LOW) # set ENPIN LOW => start control

    except KeyboardInterrupt :
        pass
    GPIO.output(ENPIN,GPIO.HIGH) # set ENPIN HIGH
    GPIO.cleanup()



