# import time
# from adafruit_servokit import ServoKit

# # Set channels to the number of servo channels on your kit.
# # 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
# kit = ServoKit(channels=16)

# kit.servo[0].angle = 180
# # kit.continuous_servo[1].throttle = 1
# time.sleep(1)
# # kit.continuous_servo[1].throttle = -1
# time.sleep(1)
# kit.servo[0].angle = 0
# # kit.continuous_servo[1].throttle = 0
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This simple test outputs a 50% duty cycle PWM single on the 0th channel. Connect an LED and
# # resistor in series to the pin to visualize duty cycle changes and its impact on brightness.

# from board import SCL, SDA
# import time
# import busio

# # Import the PCA9685 module.
# from adafruit_pca9685 import PCA9685

# print(PCA9685)
# # Create the I2C bus interface.
# i2c_bus = busio.I2C(SCL, SDA)
# print(i2c_bus)

# # Create a simple PCA9685 class instance.
# pca = PCA9685(i2c_bus)
# print(pca)
# # Set the PWM frequency to 60hz.
# pca.frequency = 50
# print(pca.frequency)

# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.
# while True :
#     pca.channels[0].duty_cycle = 0x4cc #5%
#     time.sleep(1)
#     # pca.channels[1].duty_cycle = 0x4cc #5%
#     # time.sleep(1)
#     # pca.channels[2].duty_cycle = 0x4cc #5%
#     # time.sleep(1)
#     pca.channels[0].duty_cycle = 0x1fff #10%
#     time.sleep(1)
#     # pca.channels[1].duty_cycle = 0x1fff #10%
#     # time.sleep(1)
#     # pca.channels[2].duty_cycle = 0x1fff #10%
#     # time.sleep(1)
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
kit.servo[0].angle=137
kit.servo[0].angle=25
quit()
