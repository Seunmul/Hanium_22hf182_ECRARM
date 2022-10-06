from __control__ import Arm
from __calculation__ import CALCUL
# from __control__ import GPIO
# Import python Internal library
from threading import Thread
import RPi.GPIO as GPIO
import time

if __name__ == "__main__":
    print("initializing....")
    # GPIO.cleanup() 
    Arm = Arm()
    CALCUL = CALCUL()

    Arm._STEP_SETUP_()
    Arm._SERVO_SETUP_() 
    Arm._INIT_()
    Arm.setElectromagnetic()

    try:
        # iter = 0
        # while(1) :
        #     if iter == 1 :
        #         GPIO.output(Arm.ELCTROMAGNETIC, GPIO.LOW)
        #         time.sleep(1.5)
        #     else :    
        #         GPIO.output(Arm.ELCTROMAGNETIC, GPIO.HIGH)
        #         time.sleep(1.5)
        #     iter = (iter + 1)%2    
    
        while True :

            ##-------------------------------------각도 직접 입력 -------------------------------------------------------------
            print("각도 제한 범위 : -180<theta0<180, 0<theta1<174, -58<theta2<90 , 0<theta3<90, 0<theta4<180, 0<theta5<180 ")
            print("현재 각도 : " + str(Arm.getCurDegree()))
            theta0, theta1, theta2, theta3  = map(int, input("관절 이동각도 입력 (x, y, z, w) : ").split())

            X_axis = Thread(name="X_axis", target=Arm._STEP_CONTROL_, args=(
                "X", theta0 , Arm.STEPPIN_X, Arm.DIRPIN_X, Arm.ENPIN_X,), daemon=True)
            Y_axis = Thread(name="Y_axis", target=Arm._STEP_CONTROL_, args=(
                "Y", theta1, Arm.STEPPIN_Y, Arm.DIRPIN_Y, Arm.ENPIN_Y,), daemon=True)
            Z_axis = Thread(name="Z_axis", target=Arm._STEP_CONTROL_, args=(
                "Z", theta2, Arm.STEPPIN_Z, Arm.DIRPIN_Z, Arm.ENPIN_Z,), daemon=True)
            W_axis = Thread(name="W_axis", target=Arm._SERVO_CONTROL_, args=(
                "W", theta3, Arm.PCA_CHANNEL_W, Arm.MIN_PWM_W, Arm.INTERVAL_W,), daemon=True) 
            Axises = [X_axis, Y_axis, Z_axis, W_axis]             

            Axises[0].start()
            Axises[0].join()

            Axises[1].start()
            Axises[2].start()
            Axises[1].join()
            Axises[2].join()

            Axises[3].start()
            Axises[3].join()
            Arm.updateCurDegree()

    except KeyboardInterrupt:
        pass
    finally:
        print("\n\nback to initialize state...")
        # Arm._FIN_()
        print(Arm.getCurDegree())
        print("GPIO CLEAN")
        #GPIO.cleanup() 
        print("End")
