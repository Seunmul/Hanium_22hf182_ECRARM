#######################################################333
# 각도는 + 방향이 앞으로 꺾이는 방향, 


# Import RPi lib
import RPi.GPIO as GPIO

# Import 3rd party module lib : adafruit
import busio as BUSIO
from board import SCL, SDA  # Import board module info
from adafruit_pca9685 import PCA9685  # Import the PCA9685 module.

# Import python Internal library
import time
from threading import Thread
from threading import Timer
from queue import Queue


def stepPinTimer(STEPPIN, GPIO_OUT, i):
    print("status : %d | count : %d" %(GPIO_OUT,i))
    GPIO.output(STEPPIN,GPIO_OUT)
    return

# class


class Arm:

    # step control pins
    STEPPIN_X, DIRPIN_X, ENPIN_X = 5, 6, 13  # BOARD 29 31 33
    STEPPIN_Y, DIRPIN_Y, ENPIN_Y = 12, 16, 20  # BOARD 32 36 38
    STEPPIN_Z, DIRPIN_Z, ENPIN_Z = 19, 26, 21  # BOARD 35 37 40
    STEP_MODE_PIN_x = 14  # BOARD : 8
    STEP_MODE_PIN_z = 17  # BOARD : 11
    STEP_VCC_PIN = 15  # BOARD : 10

    # step moter contorl params
    STEP_MODE = 16  # step motor mode
    STEP_FREQ = 500  # step moter signal frequency
    PINS = [STEPPIN_X, DIRPIN_X, ENPIN_X,
            STEPPIN_Y, DIRPIN_Y, ENPIN_Y,
            STEPPIN_Z, DIRPIN_Z, ENPIN_Z,
            STEP_MODE_PIN_x, STEP_MODE_PIN_z, STEP_VCC_PIN]
    SLEEPTIME = 1  # 스텝모터 구동 간 sleep타임

    # sero control parms
    PCA_CHANNEL_W, PCA_CHANNEL_R, PCA_CHANNEL_S = 0, 1, 2
    INTERVAL_W, MIN_PWM_W, MAX_PWM_W = 0, 0, 0
    INTERVAL_R, MIN_PWM_R, MAX_PWM_R = 0, 0, 0
    INTERVAL_S, MIN_PWM_S, MAX_PWM_S = 0, 0, 0

    def __init__(self):
        I2C_BUS=BUSIO.I2C(SCL, SDA)
        PCA = PCA9685(I2C_BUS)  # Create a simple PCA9685 class instance.
        PCA.frequency = 60  # Set the PWM frequency to 60hz.

        self.que = Queue()
        self.degree = {"X": 0, "Y": 180, "Z": -30, "W": 10, "R": 0, "S" : 0 } 
        self.init_degree = {"X": 0, "Y": 180, "Z": -30, "W": 10, "R": 0, "S" : 0}
        self.sort_buckets = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        self.PCA = PCA
        return

    def getCurDegree(self):
        # print(self.degree)
        return self.degree

    def getDegreeQueue(self):
        return self.que

    def updateCurDegree(self):
        while self.que.empty() == False:
            self.degree.update(self.que.get())
        return 

    def _INIT_(self): # 무슨 각도에 있든지 초기 상태로 돌리는 함수
        self._SERVO_CONTROL_("S", (self.init_degree.get('S')-self.degree.get('S')) , Arm.PCA_CHANNEL_S, Arm.MIN_PWM_S, Arm.INTERVAL_S)
        self._SERVO_CONTROL_("R", (self.init_degree.get('R')-self.degree.get('R')) , Arm.PCA_CHANNEL_R, Arm.MIN_PWM_R, Arm.INTERVAL_R)
        self._SERVO_CONTROL_("W", (self.init_degree.get('W')-self.degree.get('W')) , Arm.PCA_CHANNEL_W, Arm.MIN_PWM_W, Arm.INTERVAL_W)
        self._STEP_CONTROL_("Z", (self.init_degree.get('Z')-self.degree.get('Z')) , Arm.STEPPIN_Z, Arm.DIRPIN_Z, Arm.ENPIN_Z)
        self._STEP_CONTROL_("Y", (self.init_degree.get('Y')-self.degree.get('Y')) , Arm.STEPPIN_Y, Arm.DIRPIN_Y, Arm.ENPIN_Y)
        self._STEP_CONTROL_("X", (self.init_degree.get('X')-self.degree.get('X')) , Arm.STEPPIN_X, Arm.DIRPIN_X, Arm.ENPIN_X)
        print("initializing complete! ")
        self.updateCurDegree()
        return    

    # -180<x<180, 0<y<180, -30<z<90 , 0<w<180, 0<r<180
    def checkAngle(self ,degree, AXIS) :
        pre_degree = self.degree.get(AXIS)
        angle = pre_degree + degree

        if AXIS == 'X' and ( angle < -180  or angle > 180) :
            return ( -180 - pre_degree ) if angle < -180 else ( 180 - pre_degree ) # 360 up re
        elif AXIS == 'Y' and ( angle < 0  or angle > 180) :
            return (0 - pre_degree) if angle < 0 else (180 - pre_degree)
        elif AXIS == 'Z' and ( angle < -30  or angle > 90) :
            return (-30 - pre_degree) if angle < -30 else (90 - pre_degree)
        elif AXIS == 'W' and ( angle < 0 or angle > 180) :
            return (0 - pre_degree) if  angle < 0 else (180 - pre_degree)
        elif AXIS == 'R' and ( angle < 0  or angle > 180) :
            return (0 - pre_degree) if angle < 0 else (180 - pre_degree) 
        elif AXIS == 'S' and ( angle < 0  or angle > 180) :
            return (0 - pre_degree) if angle < 0 else (180 - pre_degree)     
        else :
            return degree    
    # STEP ---------------------------------------------------------

    def _STEP_SETUP_(self, PINS=PINS, STEP_FREQ=STEP_FREQ, STEP_MODE=STEP_MODE,
                     STEP_VCC_PIN=STEP_VCC_PIN):          
        
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
        for PIN in PINS:
            GPIO.setup(PIN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.output(PINS[9], GPIO.HIGH)
        GPIO.output(PINS[10], GPIO.HIGH)
        GPIO.output(STEP_VCC_PIN, GPIO.HIGH)
        self.STEP_PULSE_LEVEL_TIME = STEP_PULSE_LEVEL_TIME
        self.STEP_MODE = STEP_MODE
        return STEP_PULSE_LEVEL_TIME

        # 각도=>스텝 수로 변환 // mode=>풀스텝 시 1, 하프스텝시 2 .... 마이크로스텝에 따라 8,16 ....

    def _DEGREE_TO_STEPS_(self, degree, AXIS):
        dir = 1
        # dir = GPIO.HIGH
        if(degree < 0):
            degree = abs(degree)
            dir = GPIO.LOW
            dir = 0

        steps = round(float(degree)*(int(self.STEP_MODE)/1.8), 0)
        
        # gear 에 따른 offset 
        if AXIS == 'X' :
            steps = steps * 9
        elif AXIS == 'Y':
            steps = steps * 6
        elif AXIS == 'Z' :
            steps = steps * 4.5

        # 오차 방지를 위해 정수로 반올림
        return steps , dir

    def _STEP_CONTROL_(self, AXIS, degree, STEPPIN, DIRPIN, ENPIN):
        degree = self.checkAngle(degree, AXIS)
        steps, dir = self._DEGREE_TO_STEPS_(
            degree, AXIS)  # target degree가 크면 시계방향으로 회전
        print("CONTROL %s : START || steps , dir - %s , %s" %
              (AXIS, steps, dir))

        GPIO.output(ENPIN, GPIO.LOW)
        GPIO.output(DIRPIN, dir)
        for _ in range(0, int(steps)):
            GPIO.output(STEPPIN, GPIO.HIGH)
            time.sleep(self.STEP_PULSE_LEVEL_TIME)
            GPIO.output(STEPPIN, GPIO.LOW)
            time.sleep(self.STEP_PULSE_LEVEL_TIME)
        print("CONTROL %s : END" % (AXIS))
        #  GPIO.output(ENPIN, GPIO.HIGH)  # set ENPIN HIGH
        change = degree + self.degree.get(AXIS)
        self.que.put({AXIS: change})
        return

    # SERVO---------------------------------------------------------

    def _DEGREE_TO_PWM_(self, interval, min_pwm, degree):
        pwm = min_pwm + (interval*180) if degree > 180 else min_pwm + \
            (interval*degree)
        return pwm

    def _SERVO_SETUP_(self, MIN=0x07f5, MAX=0x1b6f):
        degree_per_interval = round(float(MAX-MIN)/180, 1)
        # print("%f %d %d\n" % (degree_per_interval, MIN, MAX))
        Arm.INTERVAL_W , Arm.INTERVAL_R, Arm.INTERVAL_S = degree_per_interval, degree_per_interval, degree_per_interval
        Arm.MIN_PWM_W, Arm.MIN_PWM_R,  Arm.MIN_PWM_S = MIN, MIN, MIN
        Arm.MAX_PWM_W , Arm.MAX_PWM_R,  Arm.MAX_PWM_S = MAX, MAX, MAX 
        return 

    def _SERVO_CONTROL_(self, AXIS, degree, channel_num, min_pwm, interval):
        print("CONTROL %s : START" % (AXIS))
        degree = self.checkAngle(degree, AXIS)
        cur_pwm = self._DEGREE_TO_PWM_(interval, min_pwm, self.degree.get(AXIS))
        pwm = self._DEGREE_TO_PWM_(interval, min_pwm, degree + self.degree.get(AXIS))
        print("목표 pwm :  %d " % (pwm))
        if(cur_pwm < pwm):
            while cur_pwm < pwm:
                cur_pwm = cur_pwm + interval if((cur_pwm + interval) < pwm) else pwm
                self.PCA.channels[channel_num].duty_cycle = int(cur_pwm)
                time.sleep(0.005)
                print("%d \n" , cur_pwm)
        elif(cur_pwm > pwm):
            while cur_pwm > pwm:
                cur_pwm = cur_pwm - interval if((cur_pwm-interval) > pwm) else pwm
                self.PCA.channels[channel_num].duty_cycle = int(cur_pwm)
                time.sleep(0.005)
                print("%d \n" , cur_pwm)

        print("check pwm : %d" % (pwm))
        print("CONTROL %s : END" % (AXIS))

        change = self.degree.get(AXIS) + degree
        self.que.put({AXIS: change})
        return 

## 입력한 각도만큼 돌아가게 만듦