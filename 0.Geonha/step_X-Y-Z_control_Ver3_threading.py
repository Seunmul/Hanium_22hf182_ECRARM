#import libraries
import RPi.GPIO as GPIO
import time
from threading import Thread


def __SETUP__(PINS, FREQ=60, MOTOR_MODE=1):

    print("\nsetup.....")
    # set GPIO mode => BOARD, BOARD GPIO = physical GPIO
    GPIO.setmode(GPIO.BOARD)
    # set Pins number
    PINS = PINS
    # set motor pulse & rpm of step motor by input FREQ
    FREQ = FREQ
    INTERVAL_TIME = FREQ ** -1
    MOTOR_PULSE = round(INTERVAL_TIME/2, 6)

    print("스텝모터 구동방식(풀스텝=1, 하프스텝=2 ...) : " + str(MOTOR_MODE))
    print("스텝모터 펄스 주파수 : " + str(round(FREQ, 3)) + "Hz")
    print("스텝모터 펄스 주기 : " + str(INTERVAL_TIME) + "sec")
    print("스텝모터 분당회전속도 : " + str(round(1.8/MOTOR_MODE/360*FREQ*60, 3)) + "rpm")
    print("스텝모터 펄스레벨 변화주기 : " + str(MOTOR_PULSE)+"sec\n")

    # setup GPIO PINS
    for PIN in PINS:
        print(PIN, end=" ")
        # GPIO PIN number에 맞게 셋업 : GPIO.OUT / GPIO.IN
        GPIO.setup(PIN, GPIO.OUT, initial=GPIO.LOW)
    print("\nsetup completed\n")

    return MOTOR_PULSE


def __CONTROL_X__(STEP, STEPPIN, DIRPIN, ENPIN, MOTOR_SPEED=0.0001):

    STEP = int(STEP)
    GPIO.output(ENPIN, GPIO.LOW)  # set ENPIN LOW => start control
    print("__CONTROL_X : START")
    for i in range(0, STEP):
        GPIO.output(STEPPIN, GPIO.LOW)
        time.sleep(MOTOR_SPEED)
        GPIO.output(STEPPIN, GPIO.HIGH)
        time.sleep(MOTOR_SPEED)
        # print(i,end=" ")
    print("__CONTROL_X : END\n")
    GPIO.output(ENPIN, GPIO.HIGH)  # set ENPIN HIGH
    time.sleep(SLEEPTIME)

    return


def __CONTROL_Y__(STEP, STEPPIN, DIRPIN, ENPIN, MOTOR_SPEED=0.0001):

    STEP = int(STEP)
    GPIO.output(ENPIN, GPIO.LOW)  # set ENPIN LOW => start control
    print("__CONTROL_Y : START")
    for i in range(0, STEP):
        GPIO.output(STEPPIN, GPIO.LOW)
        time.sleep(MOTOR_SPEED)
        GPIO.output(STEPPIN, GPIO.HIGH)
        time.sleep(MOTOR_SPEED)
        # print(i,end=" ")
    print("__CONTROL_Y : END\n")
    GPIO.output(ENPIN, GPIO.HIGH)  # set ENPIN HIGH
    time.sleep(SLEEPTIME)

    return


def __CONTROL_Z__(STEP, STEPPIN, DIRPIN, ENPIN, MOTOR_SPEED=0.0001):

    STEP = int(STEP)
    GPIO.output(ENPIN, GPIO.LOW)  # set ENPIN LOW => start control
    print("__CONTROL_Z : START")
    for i in range(0, STEP):
        GPIO.output(STEPPIN, GPIO.LOW)
        time.sleep(MOTOR_SPEED)
        GPIO.output(STEPPIN, GPIO.HIGH)
        time.sleep(MOTOR_SPEED)
        # print(i,end=" ")
    print("__CONTROL_Z : END\n")
    GPIO.output(ENPIN, GPIO.HIGH)  # set ENPIN HIGH
    time.sleep(SLEEPTIME)

    return


# 각도=>스텝 수로 변환 // mode=>풀스텝 시 1, 하프스텝시 2 .... 마이크로스텝에 따라 8,16 ....
def _DEGREE_TO_STEPS_(degree=360, mode=1):
    # 소수첫째자리까지 스텝수 계산
    steps = round(float(degree)*(mode/1.8), 1)
    # 오차 방지를 위해 정수로 반올림
    return int(round(steps, 0))


if __name__ == "__main__":
    print("step-X-Y-Z control.py")
    # control params
    STEPPIN_X, DIRPIN_X, ENPIN_X = 29, 31, 33
    STEPPIN_Y, DIRPIN_Y, ENPIN_Y = 32, 36, 38
    STEPPIN_Z, DIRPIN_Z, ENPIN_Z = 35, 37, 40
    # stepmoter contorl params
    MOTOR_MODE = 8
    FREQ = 5000
    PINS = [STEPPIN_X, DIRPIN_X, ENPIN_X, STEPPIN_Y,
            DIRPIN_Y, ENPIN_Y, STEPPIN_Z, DIRPIN_Z, ENPIN_Z]
    # 구동 간 sleep타임
    SLEEPTIME = 1
    # pin setup=> 성공하면 펄스레벨 유지시간 상수 반환
    PULSE_LEVEL_TIME = __SETUP__(PINS, FREQ, MOTOR_MODE)

    # set ENPIN LOW => start control
    GPIO.output(ENPIN_X, GPIO.LOW)
    GPIO.output(ENPIN_Y, GPIO.LOW)
    GPIO.output(ENPIN_Z, GPIO.LOW)
    print("start\n")
    try:
        while True:
            # 사용자 입력 받기
            STEPS = _DEGREE_TO_STEPS_(degree=input(
                "각도를 입력하세요(0-360) : "), mode=MOTOR_MODE)
            print("steps : "+str(STEPS))

            #시간체크
            start_time = time.time()

            #__CONTROL _X:THREAD
            GPIO.output(DIRPIN_X, GPIO.HIGH)
            X_axis = Thread(name="X_axis", target=__CONTROL_X__, args=(STEPS, STEPPIN_X,
                          DIRPIN_X, ENPIN_X, PULSE_LEVEL_TIME))
            print(X_axis.name)

            #__CONTROL _Y:THREAD
            GPIO.output(DIRPIN_X, GPIO.HIGH)
            Y_axis = Thread(name="Y_axis", target=__CONTROL_Y__, args=(STEPS, STEPPIN_Y,
                          DIRPIN_Y, ENPIN_Y, PULSE_LEVEL_TIME))
            print(Y_axis.name)

            #__CONTROL _Z:THREAD
            GPIO.output(DIRPIN_X, GPIO.HIGH)
            Z_axis = Thread(name="Z_axis", target=__CONTROL_Z__, args=(STEPS, STEPPIN_Z,
                          DIRPIN_Z, ENPIN_Z, PULSE_LEVEL_TIME))
            print(Z_axis.name)

            #start control thread
            X_axis.start()
            Y_axis.start()
            Z_axis.start()

            X_axis.join()
            Y_axis.join()
            Z_axis.join()

            #소요 시간 출력
            print("--- %s seconds ---" % (time.time() - start_time))

            #stop
            print("stop")
            time.sleep(3)
            print("restart\n-----\n")

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.output(ENPIN_X, GPIO.HIGH)  # set ENPIN HIGH
        GPIO.output(ENPIN_Y, GPIO.HIGH)  # set ENPIN HIGH
        GPIO.output(ENPIN_Z, GPIO.HIGH)  # set ENPIN HIGH
        GPIO.cleanup()


            # # __CONTROL _X
            # GPIO.output(DIRPIN_X, GPIO.HIGH)
            # print("\nstart clockwise : X")
            # __CONTROL_X__(STEPS, STEPPIN_X,
            #               DIRPIN_X, ENPIN_X, MOTOR_PULSE)
            # print("start counterclockwise : X")
            # GPIO.output(DIRPIN_X, GPIO.LOW)
            # __CONTROL_X__(STEPS, STEPPIN_X,
            #               DIRPIN_X, ENPIN_X, MOTOR_PULSE)

            # # __CONTROL _Y
            # GPIO.output(DIRPIN_Y, GPIO.HIGH)
            # print("start clockwise : Y")
            # __CONTROL_Y__(STEPS, STEPPIN_Y,
            #               DIRPIN_Y, ENPIN_Y, MOTOR_PULSE)
            # print("start counterclockwise : Y")
            # GPIO.output(DIRPIN_Y, GPIO.LOW)
            # __CONTROL_Y__(STEPS, STEPPIN_Y,
            #               DIRPIN_Y, ENPIN_Y, MOTOR_PULSE)

            # # __CONTROL _Z
            # GPIO.output(DIRPIN_Z, GPIO.HIGH)
            # print("start clockwise : Z")
            # __CONTROL_Z__(STEPS, STEPPIN_Z,
            #               DIRPIN_Z, ENPIN_Z, MOTOR_PULSE)
            # print("start counterclockwise : Z")
            # GPIO.output(DIRPIN_Z, GPIO.LOW)
            # __CONTROL_Z__(STEPS, STEPPIN_Z,
            #               DIRPIN_Z, ENPIN_Z, MOTOR_PULSE)