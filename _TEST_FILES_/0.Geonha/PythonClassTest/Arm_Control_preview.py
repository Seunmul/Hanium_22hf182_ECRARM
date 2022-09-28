from __control__ import Arm

# Import python Internal library
import time
from threading import Thread

init_degree = {"X": 0, "Y": 0, "Z": 0, "W": 0, "R": 0}
target_degree = {"X": 0, "Y": 0, "Z": 0, "W": 0, "R": 0}

if __name__ == "__main__":
    print("Arm_Control_preview.py")
    print("initializing....")
    

    Arm = Arm(init_degree)
    Arm._STEP_SETUP_()
    Arm.INTERVAL_W, Arm.MIN_PWM_W, Arm.MAX_PWM_W=Arm._SERVO_SETUP_(MIN=0x07f5, MAX=0x1b6f)
    Arm.INTERVAL_R, Arm.MIN_PWM_R, Arm.MAX_PWM_R=Arm._SERVO_SETUP_(MIN=0x07f5, MAX=0x1b6f)
    Arm._SERVO_INITIAL_("W", 0,Arm.MIN_PWM_W, Arm.MAX_PWM_W, Arm.INTERVAL_W)
    Arm._SERVO_INITIAL_("R", 1,Arm.MIN_PWM_R, Arm.MAX_PWM_R, Arm.INTERVAL_R)

    try:
        while True:
            # 사용자 입력 받기
            print("현재 각도 : %s" % (Arm.getCurDegree()))
            target_degree.update(X=int(input("STEP - X축 각도를 입력하세요(0-360) : ")))
            target_degree.update(Y=int(input("STEP - Y축 각도를 입력하세요(0-360) : ")))
            target_degree.update(Z=int(input("STEP - Z축 각도를 입력하세요(0-360) : ")))
            target_degree.update(W=int(input("SERVO - W축 각도를입력하세요 : ")))
            target_degree.update(R=int(input("SERVO - R축 각도를입력하세요 : ")))
            print("\nTarget : %s" % (target_degree))
            # 시간체크
            start_time = time.time()

            # __CONTROL__ THREAD : X ,Y, Z, W, R
            X_axis = Thread(name="X_axis", target=Arm._STEP_CONTROL_, args=(
                "X", target_degree, Arm.STEPPIN_X, Arm.DIRPIN_X, Arm.ENPIN_X))
            Y_axis = Thread(name="Y_axis", target=Arm._STEP_CONTROL_, args=(
                "Y", target_degree, Arm.STEPPIN_Y, Arm.DIRPIN_Y, Arm.ENPIN_Y))
            Z_axis = Thread(name="Z_axis", target=Arm._STEP_CONTROL_, args=(
                "Z", target_degree, Arm.STEPPIN_Z, Arm.DIRPIN_Z, Arm.ENPIN_Z))
            W_axis = Thread(name="W_axis", target=Arm._SERVO_CONTROL_, args=(
                "W", 0, Arm.MIN_PWM_W, Arm.INTERVAL_W, target_degree))
            R_axis = Thread(name="R_axis", target=Arm._SERVO_CONTROL_, args=(
                "R", 1, Arm.MIN_PWM_R, Arm.INTERVAL_R, target_degree))

            # 배열로 쓰레드 관리
            Axises = []
            Axises.append(X_axis)
            Axises.append(Y_axis)
            Axises.append(Z_axis)
            Axises.append(W_axis)
            Axises.append(R_axis)

            # start control thread
            for Axis in Axises:
                # print(Axis.name, end=" ")
                Axis.start()
            # wait control thread
            for Axis in Axises:
                Axis.join()
            # 소요 시간 출력
            # time.sleep(SLEEPTIME)
            print("--- %s seconds ---" % (time.time() - start_time))
            Arm.updateCurDegree()

    except KeyboardInterrupt:
        pass
    finally:
        print("\n\nback to initialize state...")
        Arm._SERVO_TO_MIN_PWM_("W", 0, Arm.MIN_PWM_W, Arm.INTERVAL_W)
        Arm._SERVO_TO_MIN_PWM_("R", 1, Arm.MIN_PWM_R, Arm.INTERVAL_R)
        print("End")
        # GPIO.cleanup()