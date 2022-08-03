#import libraries
import RPi.GPIO as GPIO
import time


def __SETUP__(PINS, FREQ=60):

    # set GPIO mode => BOARD, BOARD GPIO = physical GPIO
    GPIO.setmode(GPIO.BOARD)
    # set Pins number
    PINS = PINS
    # set FREQ
    FREQ = FREQ

    # setup GPIO PINS
    for PIN in PINS:
        print(PIN)
        # GPIO PIN number에 맞게 셋업 : GPIO.OUT / GPIO.IN
        GPIO.setup(PIN, GPIO.OUT, initial=GPIO.LOW)


def __CONTROL_X__(STEP, STEPPIN, DIRPIN, ENPIN, MOTOR_SPEED=0.0001):

    STEP = int(STEP)
    GPIO.output(ENPIN, GPIO.LOW)  # set ENPIN LOW => start control
    print("__CONTROL_X : START\n")
    for i in range(0, STEP):
        GPIO.output(STEPPIN, GPIO.LOW)
        time.sleep(MOTOR_SPEED)
        GPIO.output(STEPPIN, GPIO.HIGH)
        time.sleep(MOTOR_SPEED)
        # print(i,end=" ")
    print("\n__CONTROL_X : END\n")
    GPIO.output(ENPIN, GPIO.HIGH)  # set ENPIN HIGH
    time.sleep(1)

    return


def __CONTROL_Y__(STEP, STEPPIN, DIRPIN, ENPIN, MOTOR_SPEED=0.0001):

    STEP = int(STEP)
    GPIO.output(ENPIN, GPIO.LOW)  # set ENPIN LOW => start control
    print("__CONTROL_Y : START\n")
    for i in range(0, STEP):
        GPIO.output(STEPPIN, GPIO.LOW)
        time.sleep(MOTOR_SPEED)
        GPIO.output(STEPPIN, GPIO.HIGH)
        time.sleep(MOTOR_SPEED)
        # print(i,end=" ")
    print("\n__CONTROL_Y : END\n")
    GPIO.output(ENPIN, GPIO.HIGH)  # set ENPIN HIGH
    time.sleep(1)


def __CONTROL_Z__(STEP, STEPPIN, DIRPIN, ENPIN, MOTOR_SPEED=0.0001):

    STEP = int(STEP)
    GPIO.output(ENPIN, GPIO.LOW)  # set ENPIN LOW => start control
    print("__CONTROL_Z : START\n")
    for i in range(0, STEP):
        GPIO.output(STEPPIN, GPIO.LOW)
        time.sleep(MOTOR_SPEED)
        GPIO.output(STEPPIN, GPIO.HIGH)
        time.sleep(MOTOR_SPEED)
        # print(i,end=" ")
    print("\n__CONTROL_Z : END\n")
    GPIO.output(ENPIN, GPIO.HIGH)  # set ENPIN HIGH
    time.sleep(1)


if __name__ == "__main__":
    print("step-X-Y-Z control.py")
    # control params
    STEPPIN_X, DIRPIN_X, ENPIN_X = 29, 31, 33
    STEPPIN_Y, DIRPIN_Y, ENPIN_Y = 32, 36, 38
    STEPPIN_Z, DIRPIN_Z, ENPIN_Z = 35, 37, 40

    STPES_PER_REVOLUTION = 1600
    MOTOR_SPEED = 0.0001

    FREQ = 60
    PINS = [STEPPIN_X, DIRPIN_X, ENPIN_X, STEPPIN_Y,
            DIRPIN_Y, ENPIN_Y, STEPPIN_Z, DIRPIN_Z, ENPIN_Z]

    __SETUP__(PINS, FREQ)

    GPIO.output(ENPIN_X, GPIO.LOW)  # set ENPIN LOW => start control
    GPIO.output(ENPIN_Y, GPIO.LOW)  # set ENPIN LOW => start control
    GPIO.output(ENPIN_Z, GPIO.LOW)  # set ENPIN LOW => start control
    print("start\n")
    try:
        while True:

            # __CONTROL _X
            GPIO.output(DIRPIN_X, GPIO.HIGH)
            print("start clockwise : X")
            __CONTROL_X__(STPES_PER_REVOLUTION, STEPPIN_X,
                          DIRPIN_X, ENPIN_X, MOTOR_SPEED)
            print("start counterclockwise : X")
            GPIO.output(DIRPIN_X, GPIO.LOW)
            __CONTROL_X__(STPES_PER_REVOLUTION, STEPPIN_X,
                          DIRPIN_X, ENPIN_X, MOTOR_SPEED)

            # __CONTROL _Y
            GPIO.output(DIRPIN_Y, GPIO.HIGH)
            print("start clockwise : Y")
            __CONTROL_Y__(STPES_PER_REVOLUTION, STEPPIN_Y,
                          DIRPIN_Y, ENPIN_Y, MOTOR_SPEED)
            print("start counterclockwise : Y")
            GPIO.output(DIRPIN_Y, GPIO.LOW)
            __CONTROL_Y__(STPES_PER_REVOLUTION, STEPPIN_Y,
                          DIRPIN_Y, ENPIN_Y, MOTOR_SPEED)

            # __CONTROL _Z
            GPIO.output(DIRPIN_Z, GPIO.HIGH)
            print("start clockwise : Z")
            __CONTROL_Z__(STPES_PER_REVOLUTION, STEPPIN_Z,
                          DIRPIN_Z, ENPIN_Z, MOTOR_SPEED)
            print("start counterclockwise : Z")
            GPIO.output(DIRPIN_Z, GPIO.LOW)
            __CONTROL_Z__(STPES_PER_REVOLUTION, STEPPIN_Z,
                          DIRPIN_Z, ENPIN_Z, MOTOR_SPEED)
            # print stop
            print("stop")
            time.sleep(3)
            print("restart\n-----\n")

    except KeyboardInterrupt:
        pass

    GPIO.output(ENPIN_X, GPIO.HIGH)  # set ENPIN HIGH
    GPIO.output(ENPIN_Y, GPIO.HIGH)  # set ENPIN HIGH
    GPIO.output(ENPIN_Z, GPIO.HIGH)  # set ENPIN HIGH
    GPIO.cleanup()
