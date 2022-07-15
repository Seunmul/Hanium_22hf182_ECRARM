#스텝모터 PWM 신호 인가 테스트 코드 => 
from time import sleep
import RPi.GPIO as GPIO

FREQ=50
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)


GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
PWM_PIN1 = GPIO.PWM(13,FREQ)
PWM_PIN1.start(0)
PWM_PIN2 = GPIO.PWM(15,FREQ)
PWM_PIN2.start(0)



print("step_on_off_test1")
GPIO.output(11,True)
try :
    while 1:
        PWM_PIN1.ChangeDutyCycle(50)
        sleep(0.01)
        PWM_PIN1.ChangeDutyCycle(0)
        sleep(0.01)
        PWM_PIN2.ChangeDutyCycle(50)
        sleep(0.01)
        PWM_PIN2.ChangeDutyCycle(0)
        sleep(0.01)
finally :
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(15,False)

