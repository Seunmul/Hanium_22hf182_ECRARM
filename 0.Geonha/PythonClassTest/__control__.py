# Import RPi lib
# import RPi.GPIO as GPIO

# Import 3rd party module lib : adafruit
# import busio as BUSIO
# from board import SCL, SDA  # Import board module info
# from adafruit_pca9685 import PCA9685  # Import the PCA9685 module.

# Import python Internal library
import time
from threading import Thread
from threading import Timer
from queue import Queue


def stepPinTimer(STEPPIN, GPIO_OUT, i):
    # print("status : %d | count : %d" %(GPIO_OUT,i))
    # GPIO.output(STEPPIN,GPIO_OUT)
    return

# class


class Arm:

    # BUSIO.I2C(SCL, SDA)
    # PCA = PCA9685(I2C_BUS)  # Create a simple PCA9685 class instance.
    # PCA.frequency = 60  # Set the PWM frequency to 60hz.

    # step control pins
    STEPPIN_X, DIRPIN_X, ENPIN_X = 5, 6, 13  # BOARD 29 31 33
    STEPPIN_Y, DIRPIN_Y, ENPIN_Y = 12, 16, 20  # BOARD 32 36 38
    STEPPIN_Z, DIRPIN_Z, ENPIN_Z = 19, 26, 21  # BOARD 35 37 40
    STEP_MODE_PIN = 14  # BOARD : 8
    STEP_VCC_PIN = 15  # BOARD : 10

    # step moter contorl params
    STEP_MODE = 8  # step motor mode
    STEP_FREQ = 5000  # step moter signal frequency
    PINS = [STEPPIN_X, DIRPIN_X, ENPIN_X,
            STEPPIN_Y, DIRPIN_Y, ENPIN_Y,
            STEPPIN_Z, DIRPIN_Z, ENPIN_Z, ]
    SLEEPTIME = 1  # 스텝모터 구동 간 sleep타임

    # sero control parms
    INTERVAL_R, MIN_PWM_R, MAX_PWM_R = 0, 0, 0
    INTERVAL_W, MIN_PWM_W, MAX_PWM_W = 0, 0, 0

    def __init__(self, init_degree):
        self.que = Queue()
        self.cur_degree = init_degree
        # self.PCA = PCA
        return

    def getCurDegree(self):
        # print(self.cur_degree)
        return self.cur_degree

    def getDegreeQueue(self):
        return self.que

    def updateCurDegree(self):
        while self.que.empty() == False:
            self.cur_degree.update(self.que.get())
        return
    # STEP ---------------------------------------------------------

    def _STEP_SETUP_(self, PINS=PINS, STEP_FREQ=STEP_FREQ, STEP_MODE=STEP_MODE):
        print("\nSTEPMOTOR | setup.....")

        INTERVAL_TIME = STEP_FREQ ** -1
        STEP_PULSE_LEVEL_TIME = round(INTERVAL_TIME/2, 6)

        print("스텝모터 구동방식(풀스텝=1, 하프스텝=2 ...) : " + str(STEP_MODE))
        print("스텝모터 펄스 주파수 : " + str(round(STEP_FREQ, 3)) + "Hz")
        print("스텝모터 펄스 주기 : " + str(INTERVAL_TIME) + "sec")
        print("스텝모터 분당회전속도 : " +
              str(round(1.8/STEP_MODE/360*STEP_FREQ*60, 3)) + "rpm")
        print("스텝모터 펄스레벨 변화주기 : " + str(STEP_PULSE_LEVEL_TIME)+"sec\n")

        # GPIO PIN number에 맞게 셋업 : GPIO.OUT / GPIO.IN
        # for PIN in PINS:
        #     GPIO.setup(PIN, GPIO.OUT, initial=GPIO.LOW)

        self.STEP_PULSE_LEVEL_TIME = STEP_PULSE_LEVEL_TIME
        self.STEP_MODE = STEP_MODE
        return STEP_PULSE_LEVEL_TIME

        # 각도=>스텝 수로 변환 // mode=>풀스텝 시 1, 하프스텝시 2 .... 마이크로스텝에 따라 8,16 ....

    def _DEGREE_TO_STEPS_(self, degree):
        dir = 1
        # dir = GPIO.HIGH
        if(degree < 0):
            degree = abs(degree)
            # dir = GPIO.LOW
            dir = 0

        # 오차 방지를 위해 정수로 반올림
        return round(float(degree)*(int(self.STEP_MODE)/1.8), 0), dir

    def _STEP_CONTROL_(self, AXIS, target_degree, STEPPIN, DIRPIN, ENPIN):
        cur_degree = self.cur_degree.get(AXIS, "No current Axis")
        target_degree = target_degree.get(AXIS, "No target Axis")
        steps, dir = self._DEGREE_TO_STEPS_(
            target_degree-cur_degree)  # target degree가 크면 시계방향으로 회전
        print("CONTROL %s : START || steps , dir - %s , %s" %
              (AXIS, steps, dir))

        # GPIO.output(ENPIN, GPIO.LOW)
        # GPIO.output(DIRPIN, dir)
        for i in range(0, int(steps)):

            on = Timer(self.STEP_PULSE_LEVEL_TIME,
                       stepPinTimer, (STEPPIN, 1, i))
            on.start()
            on.join()

            off = Timer(self.STEP_PULSE_LEVEL_TIME,
                        stepPinTimer, (STEPPIN, 0, i))
            off.start()
            off.join()

            # GPIO.output(STEPPIN, GPIO.HIGH)
            # time.sleep(self.STEP_PULSE_LEVEL_TIME)
            # GPIO.output(STEPPIN, GPIO.LOW)
            # time.sleep(self.STEP_PULSE_LEVEL_TIME)
        print("CONTROL %s : END" % (AXIS))
        # GPIO.output(ENPIN, GPIO.HIGH)  # set ENPIN HIGH
        self.que.put({AXIS: target_degree})
        return

    # SERVO---------------------------------------------------------

    def _DEGREE_TO_PWM_(self, interval, min_pwm, degree):
        pwm = min_pwm + (interval*180) if degree > 180 else min_pwm + \
            (interval*degree)
        return pwm

    def _SERVO_SETUP_(self, MIN, MAX):
        degree_per_interval = round(float(MAX-MIN)/180, 1)
        # print("%f %d %d\n" % (degree_per_interval, MIN, MAX))
        return degree_per_interval, MIN, MAX

    def _SERVO_TO_MIN_PWM_(self, AXIS, channel_num, min_pwm, interval):
        cur_degree = self.cur_degree.get(AXIS, "No current Axis")
        print("MIN PWM %s AXIS " % (AXIS), end=" ")
        cur_pwm = self._DEGREE_TO_PWM_(interval, min_pwm, cur_degree)
        while cur_pwm > min_pwm:
            cur_pwm = cur_pwm - \
                interval if((cur_pwm-interval) > min_pwm) else min_pwm
            #self.PCA.channels[channel_num].duty_cycle = int(cur_pwm)
            time.sleep(0.001)
        print("min pwm : %d " % (cur_pwm))
        self.que.put({AXIS: 0})
        return cur_pwm

    def _SERVO_TO_MAX_PWM_(self, AXIS, channel_num, min_pwm, max_pwm, interval):
        cur_degree = self.cur_degree.get(AXIS, "No current Axis")
        print("MAX PWM %s AXIS " % (AXIS), end=" ")
        cur_pwm = self._DEGREE_TO_PWM_(interval, min_pwm, cur_degree)
        while cur_pwm < max_pwm:
            cur_pwm = cur_pwm + \
                interval if((cur_pwm+interval) < max_pwm) else max_pwm
            #self.PCA.channels[channel_num].duty_cycle = int(cur_pwm)
            time.sleep(0.001)
        print("max pwm : %d " % (cur_pwm))
        self.que.put({AXIS: 180})
        return cur_pwm

    def _SERVO_INITIAL_(self, AXIS, channel_num, min_pwm, max_pwm, interval):
        cur_degree = self.cur_degree.get(AXIS, "No current Axis")
        print("INITALIZE %s AXIS " % (AXIS))
        cur_pwm = self._SERVO_TO_MIN_PWM_(
            AXIS, channel_num, min_pwm, interval)
        time.sleep(1)
        cur_pwm = self._SERVO_TO_MAX_PWM_(
            AXIS, channel_num, min_pwm, max_pwm, interval)
        print("initial pwm : %s\n" % (cur_pwm))

        return

    def _SERVO_CONTROL_(self, AXIS, channel_num, min_pwm, interval, target_degree):
        cur_degree = self.cur_degree.get(AXIS, "No current Axis")
        target_degree = target_degree.get(AXIS, "No target Axis")

        print("CONTROL %s : START" % (AXIS))
        cur_pwm = self._DEGREE_TO_PWM_(interval, min_pwm, cur_degree)
        target_pwm = self._DEGREE_TO_PWM_(interval, min_pwm, target_degree)
        print("현재 | 목표 pwm :  %d | %d" % (cur_pwm, target_pwm))
        if(cur_pwm < target_pwm):
            while cur_pwm < target_pwm:
                cur_pwm = cur_pwm + interval \
                    if((cur_pwm + interval) < target_pwm) else target_pwm
                #self.PCA.channels[channel_num].duty_cycle = int(cur_pwm)
                time.sleep(0.005)
        elif(cur_pwm > target_pwm):
            while cur_pwm > target_pwm:
                cur_pwm = cur_pwm - interval \
                    if((cur_pwm-interval) > target_pwm) else target_pwm
                #self.PCA.channels[channel_num].duty_cycle = int(cur_pwm)
                time.sleep(0.005)
        print("CONTROL %s : END" % (AXIS))
        print(cur_pwm)
        self.que.put({AXIS: target_degree})
        return cur_pwm
