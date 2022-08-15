# Import RPi lib
import RPi.GPIO as GPIO

# Import python Internal library
import time
from threading import Thread


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


if __name__ == "__main__":
    print("step-X-Y-Z control Ver3.py")
    # control params
    STEPPIN_X, DIRPIN_X, ENPIN_X = 5, 6, 13  # BCM
    STEPPIN_Y, DIRPIN_Y, ENPIN_Y = 12, 16, 20  # BCM
    STEPPIN_Z, DIRPIN_Z, ENPIN_Z = 19, 26, 21  # BCM
    # STEPPIN_X, DIRPIN_X, ENPIN_X = 29, 31, 33
    # STEPPIN_Y, DIRPIN_Y, ENPIN_Y = 32, 36, 38
    # STEPPIN_Z, DIRPIN_Z, ENPIN_Z = 35, 37, 40
    # stepmoter contorl params
    MOTOR_MODE = 8
    FREQ = 5000
    PINS = [STEPPIN_X, DIRPIN_X, ENPIN_X, STEPPIN_Y,
            DIRPIN_Y, ENPIN_Y, STEPPIN_Z, DIRPIN_Z, ENPIN_Z]
    # 구동 간 sleep타임
    SLEEPTIME = 1
    # pin setup=> 성공하면 펄스레벨 유지시간 상수 반환
    STEP_PULSE_LEVEL_TIME = _STEP_SETUP_(PINS, FREQ, MOTOR_MODE)

    print("start\n")
    try:
        while True:
            # 사용자 입력 받기
            steps, dir = _DEGREE_TO_STEPS_(
                degree=int(input("각도를 입력하세요(0-360) : ")),
                mode=MOTOR_MODE)
            print("steps : %d dir : %d" % (steps, dir))

            # 시간체크
            start_time = time.time()

            # __CONTROL _X:THREAD , Y:THREAD , Z:THREAD
            X_axis = Thread(name="X_axis", target=_STEP_CONTROL_, args=("X", steps, dir, STEPPIN_X,
                                                                        DIRPIN_X, ENPIN_X, STEP_PULSE_LEVEL_TIME))
            Y_axis = Thread(name="Y_axis", target=_STEP_CONTROL_, args=("Y", steps, dir, STEPPIN_Y,
                                                                        DIRPIN_Y, ENPIN_Y, STEP_PULSE_LEVEL_TIME))
            Z_axis = Thread(name="Z_axis", target=_STEP_CONTROL_, args=("Z", steps, dir, STEPPIN_Z,
                                                                        DIRPIN_Z, ENPIN_Z, STEP_PULSE_LEVEL_TIME))
            # 배열로 쓰레드 관리
            Axises = []
            Axises.append(X_axis)
            Axises.append(Y_axis)
            Axises.append(Z_axis)

            # start control thread
            for Axis in Axises:
                print(Axis.name)
                Axis.start()

            # wait control thread
            for Axis in Axises:
                Axis.join()

            time.sleep(SLEEPTIME)
            # 소요 시간 출력
            print("--- %s seconds ---" % (time.time() - start_time))

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
