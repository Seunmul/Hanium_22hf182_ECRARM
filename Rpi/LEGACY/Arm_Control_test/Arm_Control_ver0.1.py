import __Motor_Control__ as CONTROL

# Import python Internal library
import time
from threading import Thread

GPIO = CONTROL.GPIO

# Create the I2C bus interface, initialize I2C BUS with PCA9685
I2C_BUS = CONTROL.BUSIO.I2C(CONTROL.SCL, CONTROL.SDA)
# Create a simple PCA9685 class instance.
PCA = CONTROL.PCA9685(I2C_BUS)
# Set the PWM frequency to 60hz.
PCA.frequency = 60

# step control pins
STEPPIN_X, DIRPIN_X, ENPIN_X = 5, 6, 13  # BOARD 29 31 33
STEPPIN_Y, DIRPIN_Y, ENPIN_Y = 12, 16, 20  # BOARD 32 36 38
STEPPIN_Z, DIRPIN_Z, ENPIN_Z = 19, 26, 21  # BOARD 35 37 40
MOTOR_MODE_PIN = 14  # BOARD : 8
VCC = 15  # BOARD : 10

# step moter contorl params
MOTOR_MODE = 8  # 1,2,4,8,16,32 sets your stepping mode
MOTOR_MODE_PIN = 14  # BOARD : 8
VCC = 15  # BOARD : 10
FREQ = 5000  # Frequency of step motor control signal
PINS = [STEPPIN_X, DIRPIN_X, ENPIN_X,
        STEPPIN_Y, DIRPIN_Y, ENPIN_Y,
        STEPPIN_Z, DIRPIN_Z, ENPIN_Z, ]

# 스텝모터 구동 간 sleep타임
SLEEPTIME = 1

# sero control parms
INTERVAL_R, MIN_PWM_R, MAX_PWM_R = 0, 0, 0
INTERVAL_W, MIN_PWM_W, MAX_PWM_W = 0, 0, 0

# current_degree Dictionary
current_degree = {"X": 0, "Y": 0, "Z": 0, "W": 0, "R": 0}

if __name__ == "__main__":
    print("Arm_Control_ver0.0.py")
    print("initializing....")
    # setup step and step enable pins => 성공하면 펄스레벨 유지시간 상수 반환, GPIO PIN 모두 LOW상태
    STEP_PULSE_LEVEL_TIME = CONTROL._STEP_SETUP_(PINS, FREQ, MOTOR_MODE)
    # Motor mode pin 설정 => HIGH일 경우, a4988기준 1/16제어모드
    GPIO.output(MOTOR_MODE_PIN, GPIO.HIGH)
    # login vcc핀 인가
    GPIO.output(VCC, GPIO.HIGH)

    # setup servo with pca9685, and initialize motor => return interval, min, max
    INTERVAL_R, MIN_PWM_R, MAX_PWM_R = CONTROL._SERVO_SETUP_(
        MIN=0x07f5, MAX=0x1b6f)
    INTERVAL_W, MIN_PWM_W, MAX_PWM_W = CONTROL._SERVO_SETUP_(
        MIN=0x07f5, MAX=0x1b6f)

    # servo control test
    CONTROL._SERVO_INITIAL_("W", PCA, 0, current_degree.get(
        "W", "No Axis"), MIN_PWM_W, MAX_PWM_W, INTERVAL_W)
    CONTROL._SERVO_INITIAL_("R", PCA, 1, current_degree.get(
        "R", "No Axis"), MIN_PWM_R, MAX_PWM_R, INTERVAL_R)

    print("start\n")
    try:
        while True:

            # 사용자 입력 받기
            steps, dir = CONTROL._DEGREE_TO_STEPS_(
                degree=int(input("STEP - 각도를 입력하세요(0-360) : ")),
                mode=MOTOR_MODE)
            print("steps : %d dir : %d" % (steps, dir))

            target_degree_W, target_degree_R = int(
                input("SERVO - W축 각도를입력하세요 : ")), int(input("SERVO - W축 각도를입력하세요 : "))
            # 시간체크
            start_time = time.time()

            # __CONTROL__ THREAD : X ,Y, Z, W, R
            X_axis = Thread(name="X_axis", target=CONTROL._STEP_CONTROL_, args=("X", steps, dir, STEPPIN_X,
                                                                                DIRPIN_X, ENPIN_X, STEP_PULSE_LEVEL_TIME))
            Y_axis = Thread(name="Y_axis", target=CONTROL._STEP_CONTROL_, args=("Y", steps, dir, STEPPIN_Y,
                                                                                DIRPIN_Y, ENPIN_Y, STEP_PULSE_LEVEL_TIME))
            Z_axis = Thread(name="Z_axis", target=CONTROL._STEP_CONTROL_, args=("Z", steps, dir, STEPPIN_Z,
                                                                                DIRPIN_Z, ENPIN_Z, STEP_PULSE_LEVEL_TIME))
            W_axis = Thread(name="W_axis", target=CONTROL._SERVO_CONTROL_, args=(
                "W", PCA, 0,  int(current_degree.get("W", "No Axis")), MIN_PWM_W, INTERVAL_W, target_degree_W))
            R_axis = Thread(name="R_axis", target=CONTROL._SERVO_CONTROL_, args=(
                "R", PCA, 1,  int(current_degree.get("R", "No Axis")), MIN_PWM_R, INTERVAL_R, target_degree_R))

            
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
            # 소요 시간 출력
            # time.sleep(SLEEPTIME)
            print("--- %s seconds ---" % (time.time() - start_time))

    except KeyboardInterrupt:
        pass
    finally:
        print("\n\nback to initialize state...")
        CONTROL._SERVO_TO_MIN_PWM_("W", PCA, 0, int(
            current_degree.get("W", "No Axis")), MIN_PWM_W, INTERVAL_W)
        CONTROL._SERVO_TO_MIN_PWM_("R", PCA, 1, int(
            current_degree.get("R", "No Axis")), MIN_PWM_R, INTERVAL_R)

        print("End")
        GPIO.cleanup()

        # for i in range(0, len(cur_pwms)):
        #     # 서보초기화
        #     CONTROL._SERVO_MIN_PWM_(PCA, i, cur_pwms, min_pwm, interval)
