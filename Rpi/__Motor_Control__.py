# Import RPi lib
import RPi.GPIO as GPIO

# Import 3rd party module lib : adafruit
import busio as BUSIO
from board import SCL, SDA  # Import board module info
from adafruit_pca9685 import PCA9685  # Import the PCA9685 module.

# Import python Internal library
import time
from threading import Thread

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
    # GPIO.output(ENPIN, GPIO.HIGH)  # set ENPIN HIGH

    return

# 각도=>스텝 수로 변환 // mode=>풀스텝 시 1, 하프스텝시 2 .... 마이크로스텝에 따라 8,16 ....


def _DEGREE_TO_STEPS_(degree=360, mode=1):
    dir = GPIO.HIGH
    if(degree < 0):
        degree = abs(degree)
        dir = GPIO.LOW

    # 오차 방지를 위해 정수로 반올림
    return round(float(degree)*(mode/1.8), 0), dir


def _DEGREE_TO_PWM_(interval, min_pwm, degree):
    pwm = min_pwm + (interval*180) if degree > 180 else min_pwm + \
        (interval*degree)
    return pwm


def _SERVO_SETUP_(MIN, MAX):
    degree_per_interval = round(float(MAX-MIN)/180, 1)
    print("%f %d %d\n" % (degree_per_interval, MIN, MAX))
    return degree_per_interval, MIN, MAX

# SERVO---------------------------------------------------------

def _SERVO_MIN_PWM_(PCA, channel_num, cur_pwms, min_pwm, interval):
    print("min_pwm")
    cur_pwm = cur_pwms[channel_num]
    while cur_pwm > min_pwm:
        cur_pwm = cur_pwm - \
            interval if((cur_pwm-interval) > min_pwm) else min_pwm
        PCA.channels[channel_num].duty_cycle = int(cur_pwm)
        time.sleep(0.001)
    cur_pwms[channel_num] = cur_pwm
    print("stop")
    return cur_pwm


def _SERVO_MAX_PWM_(PCA, channel_num, cur_pwms, max_pwm, interval):
    cur_pwm = cur_pwms[channel_num]
    print("max_pwm")
    while cur_pwm < max_pwm:
        cur_pwm = cur_pwm + \
            interval if((cur_pwm+interval) < max_pwm) else max_pwm
        PCA.channels[channel_num].duty_cycle = int(cur_pwm)
        time.sleep(0.001)
    cur_pwms[channel_num] = cur_pwm
    print("stop")
    return cur_pwm


def _SERVO_INITIAL_(PCA, cur_pwms, min_pwm, max_pwm, interval):
    
    W_axis_MIN = Thread(
        name="W_axis_MIN", target=_SERVO_MIN_PWM_, args=(PCA, 0, cur_pwms, min_pwm, interval))
    W_axis_MAX = Thread(
        name="W_axis_MAX", target=_SERVO_MAX_PWM_, args=(PCA, 0, cur_pwms, max_pwm, interval))
    R_axis_MIN = Thread(
        name="R_axis_MIN", target=_SERVO_MIN_PWM_, args=(PCA, 1, cur_pwms, min_pwm, interval))
    R_axis_MAX = Thread(
        name="R_axis_MAX", target=_SERVO_MAX_PWM_, args=(PCA, 1, cur_pwms, max_pwm, interval))
    # thread start and join
    W_axis_MIN.start()
    R_axis_MIN.start()
    W_axis_MIN.join()
    R_axis_MIN.join()
    time.sleep(1)
    W_axis_MAX.start()
    R_axis_MAX.start()
    W_axis_MAX.join()
    R_axis_MAX.join()

    print("\ninitial pwms : "+str(cur_pwms))
    
    return


def _SERVO_CONTROL_(PCA, channel_num, cur_pwms, interval, degree_pwm):
    cur_pwm = cur_pwms[channel_num]
    print("목표 pwm : %d" % (degree_pwm))
    if(cur_pwm < degree_pwm):
        while cur_pwm < degree_pwm:
            cur_pwm = cur_pwm + interval \
                if((cur_pwm + interval) < degree_pwm) else degree_pwm
            PCA.channels[channel_num].duty_cycle = int(cur_pwm)
            time.sleep(0.005)
    elif(cur_pwm > degree_pwm):
        while cur_pwm > degree_pwm:
            cur_pwm = cur_pwm - interval \
                if((cur_pwm-interval) > degree_pwm) else degree_pwm
            PCA.channels[channel_num].duty_cycle = int(cur_pwm)
            time.sleep(0.005)
    print("stop")
    cur_pwms[channel_num] = cur_pwm
    return cur_pwm
