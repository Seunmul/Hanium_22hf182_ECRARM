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

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

# Set the PWM frequency to 60hz.
pca.frequency = 50

# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.

while True :
    pca.channels[0].duty_cycle = 0x1fff #10%
    time.sleep(1.5)
    pca.channels[0].duty_cycle = 0x1465 #5%
    time.sleep(1.5)
    pca.channels[1].duty_cycle = 0x1265 #10%
    pca.channels[2].duty_cycle = 0x1afd #10%
    time.sleep(1)
    pca.channels[1].duty_cycle = 0x1fff #5%
    pca.channels[2].duty_cycle = 0x0f65 #5%
    time.sleep(1)

    
    #0x1fff 10% 180 degree
    #0x1265 7.5% 90 degree
    #0x4cc 5% 0 degree
