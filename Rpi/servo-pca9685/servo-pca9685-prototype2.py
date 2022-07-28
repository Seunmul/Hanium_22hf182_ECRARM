# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This simple test outputs a 50% duty cycle PWM single on the 0th channel. Connect an LED and
# resistor in series to the pin to visualize duty cycle changes and its impact on brightness.


# import RPi.GPIO as GPIO
from board import SCL, SDA
import time
import busio

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# Import multiprocessing
from multiprocessing import Process, Queue
# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

# Set the PWM frequency to 60hz.
pca.frequency = 60

# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.
max_pwm,min_pwm=0x1b6f,0x07f5
cnt=min_pwm

def multi_proc_control(num,min_pwm,max_pwm) :
    while True:
        pca.channels[num].duty_cycle = min_pwm
        time.sleep(1)
        pca.channels[num].duty_cycle = max_pwm
        time.sleep(1)
    return;

proc1 = Process(target=multi_proc_control, args=(1, 0x1b6f,0x07f5))
proc2 = Process(target=multi_proc_control, args=(2, 0x1b6f,0x07f5))
proc1.start()
proc2.start()
try :
    while True :
        # print('1')
        # pca.channels[0].duty_cycle = 0x1fff #10%
        # time.sleep(1.5)
        # print('2')
        # pca.channels[0].duty_cycle = 0x1465 #5%
        # time.sleep(1.5)
      
        
        print("최대")
        while cnt<max_pwm :
            pca.channels[0].duty_cycle = cnt #10% #channel 0 -> 중간관절
            cnt = cnt + 0x003
            time.sleep(0.001)
            print(cnt)
        print("정지(최하단)")
        time.sleep(3)
        
        print("최소")
        while cnt>min_pwm :
            pca.channels[0].duty_cycle = cnt #5% #channel 0 -> 중간관절
            cnt = cnt - 0x005
            time.sleep(0.001)
            print(cnt)
        print("정지(최상단)")
        time.sleep(3)


        # pca.channels[1].duty_cycle = 0x1265 #10%
        # pca.channels[2].duty_cycle = 0x1afd #10%
        # time.sleep(1)
        # pca.channels[1].duty_cycle = 0x1fff #5%
        # pca.channels[2].duty_cycle = 0x0f65 #5%
        # time.sleep(1)
except KeyboardInterrupt:
    
    proc1.join()
    proc2.join()
    pass

# GPIO.cleanup()
    #0x1fff 10% 180 degree
    #0x1265 7.5% 90 degree
    #0x4cc 5% 0 degree
