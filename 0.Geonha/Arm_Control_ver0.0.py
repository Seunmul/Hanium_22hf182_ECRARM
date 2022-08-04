import servo_WR_control as SERVO
import step_XYZ_control_Ver3 as STEP

# Import python Internal library
import time
from threading import Thread


# initialize I2C BUS with PCA9685
# Create the I2C bus interface.
I2C_BUS = SERVO.BUSIO.I2C(SERVO.SCL, SERVO.SDA)
PCA = SERVO.PCA9685(I2C_BUS)  # Create a simple PCA9685 class instance.
PCA.frequency = 60  # Set the PWM frequency to 60hz.
# step control pins
GPIO = STEP.GPIO
STEPPIN_X, DIRPIN_X, ENPIN_X = 5, 6, 13  # BCM
STEPPIN_Y, DIRPIN_Y, ENPIN_Y = 12, 16, 20  # BCM
STEPPIN_Z, DIRPIN_Z, ENPIN_Z = 19, 26, 21  # BCM
# step moter contorl params
MOTOR_MODE = 8
FREQ = 5000
PINS = [STEPPIN_X, DIRPIN_X, ENPIN_X, STEPPIN_Y,
        DIRPIN_Y, ENPIN_Y, STEPPIN_Z, DIRPIN_Z, ENPIN_Z]
# 스텝모터 구동 간 sleep타임
SLEEPTIME = 1

if __name__ == "__main__":
    print("Arm_Control_ver0.0.py")
    print("initializing....")

    # setup step pin => 성공하면 펄스레벨 유지시간 상수 반환
    STEP_PULSE_LEVEL_TIME = STEP._STEP_SETUP_(PINS, FREQ, MOTOR_MODE)
    # setup servo with pca9685, and initialize motor
    interval, min_pwm, max_pwm = SERVO._SERVO_SETUP_(MIN=0x07f5, MAX=0x1b6f)
    # print("%f %d %d\n" % (interval, min_pwm, max_pwm))
    cur_pwms = [0, 0]
    SERVO._SERVO_INITIAL_(PCA, cur_pwms, min_pwm, max_pwm, interval)
    print("start\n")
    try:
        while True:
            # 사용자 입력 받기
            steps, dir = STEP._DEGREE_TO_STEPS_(
                degree=int(input("STEP - 각도를 입력하세요(0-360) : ")),
                mode=MOTOR_MODE)
            print("steps : %d dir : %d" % (steps, dir))
            degree_pwm = SERVO._DEGREE_TO_PWM_(
                interval, min_pwm, degree=int(input("SERVO - 각도를입력하세요 : ")))

            # 시간체크
            start_time = time.time()

            # __CONTROL _X:THREAD , Y:THREAD , Z:THREAD
            X_axis = Thread(name="X_axis", target=STEP._STEP_CONTROL_, args=("X", steps, STEPPIN_X,
                                                                             DIRPIN_X, ENPIN_X, STEP_PULSE_LEVEL_TIME))
            Y_axis = Thread(name="Y_axis", target=STEP._STEP_CONTROL_, args=("Y", steps, STEPPIN_Y,
                                                                             DIRPIN_Y, ENPIN_Y, STEP_PULSE_LEVEL_TIME))
            Z_axis = Thread(name="Z_axis", target=STEP._STEP_CONTROL_, args=("Z", steps, STEPPIN_Z,
                                                                             DIRPIN_Z, ENPIN_Z, STEP_PULSE_LEVEL_TIME))
            W_axis = Thread(name="W_axis", target=SERVO._SERVO_CONTROL_, args=(PCA, 0, cur_pwms, interval, degree_pwm))
            R_axis = Thread(name="R_axis", target=SERVO._SERVO_CONTROL_, args=(PCA, 1, cur_pwms, interval, degree_pwm))

            # 배열로 쓰레드 관리
            Axises = []
            Axises.append(X_axis)
            Axises.append(Y_axis)
            Axises.append(Z_axis)
            Axises.append(W_axis)
            Axises.append(R_axis)
            
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
        print("\n\nback to initialize state...")
        print()
        for i in range(0, len(cur_pwms)):
            SERVO._SERVO_MIN_PWM_(PCA, i, cur_pwms, min_pwm, interval)
        print(cur_pwms)
        print("test_end")
        GPIO.cleanup()
