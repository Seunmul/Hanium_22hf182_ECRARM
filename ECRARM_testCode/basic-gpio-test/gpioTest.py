# python_board_exam.py
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11,GPIO.OUT,initial=GPIO.LOW)
try:
    while(True):
     GPIO.output(11,GPIO.HIGH)
     time.sleep(0.5)
     GPIO.output(11,GPIO.LOW)
     time.sleep(0.5)
except KeyboardInterrupt:
    print("exit GPIO controll")

GPIO.cleanup()
