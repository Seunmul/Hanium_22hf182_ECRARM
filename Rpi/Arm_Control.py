from __control__ import Arm
from __calculation__ import CALCUL

# Import python Internal library
import time
from threading import Thread

if __name__ == "__main__":
    print("initializing....")

    Arm = Arm()
    CALCUL = CALCUL()

    Arm._STEP_SETUP_()
    Arm._SERVO_SETUP_() 
       
    Arm._INIT_()

    try:
        # __CONTROL__ THREAD : X ,Y, Z, W, R
        theta0 , theta1 , theta2 , theta3 , theta4 , theta5  = 0,0,0,0,0,0
        # angles = [theta0 , theta1 , theta2 , theta3 , theta4 , theta5]

        while True:
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

            # txt 파일로 입력받음
            print("현재 각도 : %s" % (Arm.getCurDegree()))
            print("각도 제한 범위 : -180<theta0<180, 0<theta1<180, -30<theta2<90 , 0<theta3<180, 0<theta4<180, 0<theta5<180 ")
            type, x_Coordinate , y_Coordinate = map(int, input("class,x, y 좌표 \
            \nclass (x, y) : ").split())
            print('\n입력 좌표 : {"X": %d, "Y": %d} ' % (x_Coordinate, y_Coordinate))

            height = CALCUL.HEIGHT
            R, theta0 = CALCUL.changeCoordinate(x_Coordinate, y_Coordinate)

            # x 축 이동
            Axises[0].start()
            Axises[0].join()
            Arm.updateCurDegree()

            while True :
                # 루프 지점
                theta1, theta2, theta3 = CALCUL.calculAngle(R, height)

                theta1 = Arm.degree.get("Y") - theta1
                theta2 = Arm.degree.get("Z") - theta2
                theta3 = Arm.degree.get("W") - theta3

                # 중간관절
                Axises[1].start()
                Axises[2].start()
                Axises[1].join()
                Axises[2].join()
                Arm.updateCurDegree()    

                # 수직 유지 , 나눠서 동작
                Axises[3].start()
                Axises[3].join()
                Arm.updateCurDegree()

                # 라이다 값 체크 
                dis = CALCUL.detect_distance()
                if CALCUL.CHECK_DIS < dis :
                    height = height - 0.15
                else :
                    #전자석으로 집는 코드
                    break    
            
            # class 에 따라 통으로 이동
            type = CALCUL.classification(type)
            theta0 = Arm.degree.get("X") - Arm.sort_buckets[type][0]
            theta1 = Arm.degree.get("Y") - Arm.sort_buckets[type][1]
            theta2 = Arm.degree.get("Z") - Arm.sort_buckets[type][2]
            theta3 = Arm.degree.get("W") - Arm.sort_buckets[type][3]

            Axises[0].start()
            Axises[0].join()
            Axises[1].start()
            Axises[1].join()
            Axises[2].start()
            Axises[2].join()
            Axises[3].start()
            Axises[3].join()

            Arm._INIT_()

            #drop 하는 코드
    except KeyboardInterrupt:
        pass
    finally:
        print("\n\nback to initialize state...")
        Arm._INIT_()
        print(Arm.getCurDegree())
        print("End")
        # GPIO.cleanup()
