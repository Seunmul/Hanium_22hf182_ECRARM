from __control__ import Arm

# Import python Internal library
import time
from threading import Thread

if __name__ == "__main__":
    print("Arm_Control_preview.py")
    print("initializing....")

    Arm = Arm()
    Arm._STEP_SETUP_()
    Arm.INTERVAL_W, Arm.MIN_PWM_W, Arm.MAX_PWM_W = Arm._SERVO_SETUP_(
        MIN=0x07f5, MAX=0x1b6f)
    Arm.INTERVAL_R, Arm.MIN_PWM_R, Arm.MAX_PWM_R = Arm._SERVO_SETUP_(
        MIN=0x07f5, MAX=0x1b6f)
    Arm._INIT_()

    try:
        while True:
            # 사용자 입력 받기
            print("현재 각도 : %s" % (Arm.getCurDegree()))
            print("각도 제한 범위 : -180<x<180, 0<y<180, -30<z<90 , 0<w<180, 0<r<180 ")
            x_d , y_d, z_d, w_d, r_d = map(int, input("STEP, SERVO 이동 각도를 입력하세요 \
            \nX, Y, Z, W, R : ").split())
            print('\n이동 각도 : {"X": %d, "Y": %d, "Z": %d, "W": %d, "R": %d}' % (x_d , y_d, z_d, w_d, r_d))
            # 시간체크
            start_time = time.time()

            # __CONTROL__ THREAD : X ,Y, Z, W, R
            X_axis = Thread(name="X_axis", target=Arm._STEP_CONTROL_, args=(
                "X", x_d , Arm.STEPPIN_X, Arm.DIRPIN_X, Arm.ENPIN_X))
            Y_axis = Thread(name="Y_axis", target=Arm._STEP_CONTROL_, args=(
                "Y", y_d, Arm.STEPPIN_Y, Arm.DIRPIN_Y, Arm.ENPIN_Y))
            Z_axis = Thread(name="Z_axis", target=Arm._STEP_CONTROL_, args=(
                "Z", z_d, Arm.STEPPIN_Z, Arm.DIRPIN_Z, Arm.ENPIN_Z))
            W_axis = Thread(name="W_axis", target=Arm._SERVO_CONTROL_, args=(
                "W", w_d, Arm.PCA_CHANNEL_W, Arm.MIN_PWM_W, Arm.INTERVAL_W))
            R_axis = Thread(name="R_axis", target=Arm._SERVO_CONTROL_, args=(
                "R", r_d, Arm.PCA_CHANNEL_R, Arm.MIN_PWM_R, Arm.INTERVAL_R))

            # 배열로 쓰레드 관리
            Axises = [X_axis, Y_axis, Z_axis, W_axis, R_axis]

            # start control thread
            for Axis in Axises:
                # print(Axis.name, end=" ")
                Axis.start()
            # wait control thread
            for Axis in Axises:
                Axis.join()

            # update current degree
            Arm.updateCurDegree() ## 내부 degree 업데이트
            # 소요 시간 출력
            # time.sleep(SLEEPTIME)
            print("--- %s seconds ---" % (time.time() - start_time))

    except KeyboardInterrupt:
        pass
    finally:
        print("\n\nback to initialize state...")
        Arm._INIT_()
        print(Arm.getCurDegree())
        print("End")
        # GPIO.cleanup()
