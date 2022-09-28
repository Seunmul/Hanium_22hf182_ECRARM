# Import 3rd party module lib : adafruit
import busio as BUSIO
from board import SCL, SDA  # Import board module info
from adafruit_pca9685 import PCA9685  # Import the PCA9685 module.

# Import python Internal library
import time
from threading import Thread


def _DEGREE_TO_PWM_(interval, min_pwm, degree):
    pwm = min_pwm + (interval*180) if degree > 180 else min_pwm + \
        (interval*degree)
    return pwm


def _SERVO_SETUP_(MIN, MAX):
    degree_per_interval = round(float(MAX-MIN)/180, 1)
    print("%f %d %d\n" % (degree_per_interval, MIN, MAX))
    return degree_per_interval, MIN, MAX


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


if __name__ == "__main__":
    # initialize I2C BUS with PCA9685
    I2C_BUS = BUSIO.I2C(SCL, SDA)  # Create the I2C bus interface.
    PCA = PCA9685(I2C_BUS)  # Create a simple PCA9685 class instance.
    PCA.frequency = 60  # Set the PWM frequency to 60hz.
    # setting servo with pca9685, and initialize motor
    print("initializing....")
    interval, min_pwm, max_pwm = _SERVO_SETUP_(MIN=0x07f5, MAX=0x1b6f)
    
    cur_pwms = [0, 0]
    _SERVO_INITIAL_(PCA, cur_pwms, min_pwm, max_pwm, interval)

    try:
        while True:
            print("\ncurrent pwms : "+str(cur_pwms))
            degree_pwm = _DEGREE_TO_PWM_(
                interval, min_pwm, degree=int(input("각도를입력하세요 : ")))

            # threading test
            W_axis = Thread(name="W_axis", target=_SERVO_CONTROL_, args=(
                PCA, 0, cur_pwms, interval, degree_pwm))
            R_axis = Thread(name="R_axis", target=_SERVO_CONTROL_, args=(
                PCA, 1, cur_pwms, interval, degree_pwm))

            # start control thread
            W_axis.start()
            R_axis.start()

            # wait control thread
            W_axis.join()
            R_axis.join()

    except KeyboardInterrupt:
        pass

    finally:
        print("\n\nback to initialize state...")
        print()
        for i in range(0, len(cur_pwms)):
            _SERVO_MIN_PWM_(PCA, i, cur_pwms, min_pwm, interval)
        print(cur_pwms)
        print("test_end")

        # 0x1fff 10% 180 degree
        # 0x1265 7.5% 90 degree
        # 0x4cc 5% 0 degree
