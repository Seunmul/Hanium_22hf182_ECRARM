# Import RPi lib
import RPi.GPIO as GPIO

# Import 3rd party module lib : adafruit
import busio as BUSIO
from board import SCL, SDA  # Import board module info
from adafruit_pca9685 import PCA9685  # Import the PCA9685 module.

# Import python Internal library
import time
from threading import Thread
from queue import Queue

# STEP ---------------------------------------------------------


def _STEP_SETUP_(PINS, FREQ=60, MOTOR_MODE=1):
    print("\nSTEPMOTOR | setup.....")
    # set GPIO mode => BOARD, BOARD GPIO = physical GPIO
    GPIO.setmode(GPIO.BCM)
    INTERVAL_TIME = FREQ ** -1
    STEP_PULSE_LEVEL_TIME = round(INTERVAL_TIME/2, 6)

    print("스텝모터 구동방식(풀스텝=1, 하프스텝=2 ...) : " + str(MOTOR_MODE))
    print("스텝모터 펄스 주파수 : " + str(round(FREQ, 3)) + "Hz")
    print("스텝모터 펄스 주기 : " + str(INTERVAL_TIME) + "sec")
    print("스텝모터 분당회전속도 : " + str(round(1.8/MOTOR_MODE/360*FREQ*60, 3)) + "rpm")
    print("스텝모터 펄스레벨 변화주기 : " + str(STEP_PULSE_LEVEL_TIME)+"sec\n")

    # setup GPIO PINS
    for PIN in PINS:
        # GPIO PIN number에 맞게 셋업 : GPIO.OUT / GPIO.IN
        GPIO.setup(PIN, GPIO.OUT, initial=GPIO.LOW)
    # print("\nsetup completed\n")

    return STEP_PULSE_LEVEL_TIME


def _STEP_CONTROL_(AXIS, steps, dir, STEPPIN, DIRPIN, ENPIN, STEP_PULSE_LEVEL_TIME=0.0001):
    GPIO.output(DIRPIN, dir)
    GPIO.output(ENPIN, GPIO.LOW)  # set ENPIN LOW => start control
    print("CONTROL %s : START" % (AXIS))
    for i in range(0, int(steps)):
        GPIO.output(STEPPIN, GPIO.LOW)
        time.sleep(STEP_PULSE_LEVEL_TIME)
        GPIO.output(STEPPIN, GPIO.HIGH)
        time.sleep(STEP_PULSE_LEVEL_TIME)
    print("CONTROL %s : END" % (AXIS))
    

    return

# 각도=>스텝 수로 변환 // mode=>풀스텝 시 1, 하프스텝시 2 .... 마이크로스텝에 따라 8,16 ....


def _DEGREE_TO_STEPS_(degree=360, mode=1):
    dir = GPIO.HIGH
    if(degree < 0):
        degree = abs(degree)
        dir = GPIO.LOW

    # 오차 방지를 위해 정수로 반올림
    return round(float(degree)*(mode/1.8), 0), dir


# SERVO---------------------------------------------------------
def _DEGREE_TO_PWM_(interval, min_pwm, degree):
    pwm = min_pwm + (interval*180) if degree > 180 else min_pwm + \
        (interval*degree)
    return pwm


def _SERVO_SETUP_(MIN, MAX):
    degree_per_interval = round(float(MAX-MIN)/180, 1)
    print("%f %d %d\n" % (degree_per_interval, MIN, MAX))
    return degree_per_interval, MIN, MAX


def _SERVO_TO_MIN_PWM_(AXIS, PCA, channel_num, cur_degree, min_pwm, interval):
    print("MIN PWM %sAXIS " % (AXIS))
    cur_pwm = _DEGREE_TO_PWM_(interval, min_pwm, cur_degree)
    while cur_pwm > min_pwm:
        cur_pwm = cur_pwm - \
            interval if((cur_pwm-interval) > min_pwm) else min_pwm
        PCA.channels[channel_num].duty_cycle = int(cur_pwm)
        time.sleep(0.001)
    return cur_pwm


def _SERVO_TO_MAX_PWM_(AXIS, PCA, channel_num, cur_degree, min_pwm, max_pwm, interval):
    print("MAX PWM %sAXIS " % (AXIS))
    cur_pwm = _DEGREE_TO_PWM_(interval, min_pwm, cur_degree)
    while cur_pwm < max_pwm:
        cur_pwm = cur_pwm + \
            interval if((cur_pwm+interval) < max_pwm) else max_pwm
        PCA.channels[channel_num].duty_cycle = int(cur_pwm)
        time.sleep(0.001)
    return cur_pwm


def _SERVO_INITIAL_(AXIS, PCA, channel_num, cur_degree, min_pwm, max_pwm, interval):
    print("INITALIZE %sAXIS " % (AXIS))
    cur_pwm = _SERVO_TO_MIN_PWM_(
        AXIS, PCA, channel_num, cur_degree, min_pwm, interval)
    time.sleep(1)
    cur_pwm = _SERVO_TO_MAX_PWM_(
        AXIS, PCA, channel_num, cur_degree, min_pwm, max_pwm, interval)
    print("\ninitial pwms : %s" % (cur_pwm))

    return


def _SERVO_CONTROL_(AXIS, PCA, channel_num, cur_degree, min_pwm, interval, target_degree):
    print("CONTROL %s : START" % (AXIS))
    cur_pwm = _DEGREE_TO_PWM_(interval, min_pwm, cur_degree)
    target_pwm = _DEGREE_TO_PWM_(interval, min_pwm, target_degree)
    print("현재 | 목표 pwm :  %d | %d" % (cur_pwm, target_pwm))
    if(cur_pwm < target_pwm):
        while cur_pwm < target_pwm:
            cur_pwm = cur_pwm + interval \
                if((cur_pwm + interval) < target_pwm) else target_pwm
            PCA.channels[channel_num].duty_cycle = int(cur_pwm)
            time.sleep(0.005)
    elif(cur_pwm > target_pwm):
        while cur_pwm > target_pwm:
            cur_pwm = cur_pwm - interval \
                if((cur_pwm-interval) > target_pwm) else target_pwm
            PCA.channels[channel_num].duty_cycle = int(cur_pwm)
            time.sleep(0.005)
    print("CONTROL %s : END" % (AXIS))
    return cur_pwm


# class
class MOTOR:

    BUSIO.I2C(SCL, SDA)
    PCA = PCA9685(I2C_BUS)  # Create a simple PCA9685 class instance.
    PCA.frequency = 60  # Set the PWM frequency to 60hz.

    STEPPIN_X, DIRPIN_X, ENPIN_X = 5, 6, 13  # BOARD 29 31 33
    STEPPIN_Y, DIRPIN_Y, ENPIN_Y = 12, 16, 20  # BOARD 32 36 38
    STEPPIN_Z, DIRPIN_Z, ENPIN_Z = 19, 26, 21  # BOARD 35 37 40
    MOTOR_MODE_PIN = 14  # BOARD : 8
    VCC = 15  # BOARD : 10
    MOTOR_MODE = 8
    FREQ = 5000
    PINS = [STEPPIN_X, DIRPIN_X, ENPIN_X,
            STEPPIN_Y, DIRPIN_Y, ENPIN_Y,
            STEPPIN_Z, DIRPIN_Z, ENPIN_Z, ]
