from __control__ import Arm

# Import python Internal library
from threading import Thread

if __name__ == "__main__":
    print("initializing....")

    Arm = Arm()

    Arm._STEP_SETUP_()
    Arm._SERVO_SETUP_() 
    Arm._INIT_()

    try:
        while True :
            
            print("각도 제한 범위 : -180<theta0<180, 0<theta1<180, -30<theta2<90 , 0<theta3<180, 0<theta4<180, 0<theta5<180 ")
            print("현재 각도 : " + str(Arm.getCurDegree()))
            theta0, theta1, theta2, theta3 , theta4, theta5 = map(int, input("관절 이동각도 입력 (x, y, z, w, r, s) : ").split())

            X_axis = Thread(name="X_axis", target=Arm._STEP_CONTROL_, args=(
                "X", theta0 , Arm.STEPPIN_X, Arm.DIRPIN_X, Arm.ENPIN_X))
            Y_axis = Thread(name="Y_axis", target=Arm._STEP_CONTROL_, args=(
                "Y", theta1, Arm.STEPPIN_Y, Arm.DIRPIN_Y, Arm.ENPIN_Y))
            Z_axis = Thread(name="Z_axis", target=Arm._STEP_CONTROL_, args=(
                "Z", theta2, Arm.STEPPIN_Z, Arm.DIRPIN_Z, Arm.ENPIN_Z))
            W_axis = Thread(name="W_axis", target=Arm._SERVO_CONTROL_, args=(
                "W", theta3, Arm.PCA_CHANNEL_W, Arm.MIN_PWM_W, Arm.INTERVAL_W))
            R_axis = Thread(name="R_axis", target=Arm._SERVO_CONTROL_, args=(
                "R", theta4, Arm.PCA_CHANNEL_R, Arm.MIN_PWM_R, Arm.INTERVAL_R))
            S_axis = Thread(name="S_axis", target=Arm._SERVO_CONTROL_, args=(
                "S", theta5, Arm.PCA_CHANNEL_S, Arm.MIN_PWM_S, Arm.INTERVAL_S))    
            Axises = [X_axis, Y_axis, Z_axis, W_axis, R_axis, S_axis]

            # 중간관절
            Axises[0].start()
            Axises[1].start()
            Axises[2].start()
            Axises[3].start()
            Axises[0].join()
            Axises[1].join()
            Axises[2].join()
            Axises[3].join()
            Arm.updateCurDegree()
            
    except KeyboardInterrupt:
        pass
    finally:
        print("\n\nback to initialize state...")
        # Arm._INIT_()
        print(Arm.getCurDegree())
        print("End")
        # GPIO.cleanup()
