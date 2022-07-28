import RPi.GPIO as GPIO
import time
LED=4
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
for i in range(1, 20):
    GPIO.output(LED, True)
    time.sleep(1)
    GPIO.output(LED, False)
    time.sleep(1)