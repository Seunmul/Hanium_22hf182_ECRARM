import math
# import matplotlib.pyplot as plt
import numpy as np

# import board
# import busio
# import adafruit_vl53l0x

class CALCUL :
    CHECK_DIS = 1
    HEIGHT=7.7

    def __init__(self):
        # self.i2c = busio.I2C(board.SCL0, board.SDA0)
        # self.vl53 = adafruit_vl53l0x.VL53L0X(i2c)
        pass

    def detect_distance(self) :
        dis_list = []
        
        for _ in range(5) :
            distance = self.vl53.range*0.1
            dis_list.append(distance)
            print("Range: {0}cm".format(distance))

        dis_list.sort()
        total = dis_list[1:-1]
        
        return sum(total)/len(total)

    def changeCoordinate(self,x,y):
        H = 10
        ## (0,0)을 중앙 하단으로 변경 
        y = y + H     

        R = math.sqrt(math.pow(abs(x),2)+math.pow((y),2))
        theta = math.cos(y/R) if x>0  else -math.cos(y/R)
        theta = math.degrees(theta)
        return R , theta

    def calculAngle(self, px, py, a1=16, a2=17):
        rsul2 = (2*math.atan((math.sqrt(((((a1 + a2)**2) - (px**2 + py**2))/((px**2 + py**2)-((a1 - a2)**2))))))) # theta2 계산
        if rsul2 < 0: # 결과값이 음수일 경우
            theta2 = rsul2 # 양수로
        else: # 결과값이 양수일 경우
            theta2 = -rsul2 # 그대로
        theta1 = math.atan(py/px ) - math.atan(((a2*math.sin(theta2))/(a1 + a2*math.cos(theta2)))) # 결과값

        theta1 = theta1*180/math.pi
        theta2 = theta2*180/math.pi 

        # print("theta1:",math.degrees(theta1),"\n"+"theta2:", math.degrees(theta2)) # 결과값 출력

        theta3 = abs( theta1 + theta2 )
        theta2 = theta2 + 90

        # x1 = a1*math.cos(theta1) # x1 좌표
        # y1 = a1*math.sin(theta1) # y1 좌표
        # x2 = x1 + a2*math.cos(theta1+theta2) # x2 좌표
        # y2 = y1 + a2*math.sin(theta1+theta2) # y2 좌표

        # plt.xlim(-30, 50) # plot할 x축 범위
        # plt.ylim(-30, 50) # plot할 y축 범위
        # plt.plot([0, x1, x2], [0, y1, y2], 'ro-') # plot할 좌표
        # print("x1 = ", x1, "\ny1 = ", y1, "\nx2 = ", x2, "\ny2 = ", y2) # 결과값 출력
        # plt.plot(px, py, 'bo') # plot할 좌표
        # plt.show() # plot

        return theta1 ,theta2, theta3

    def classification(self, element) :
        pass     

if __name__ == '__main__':
    C = CALCUL()
    # print( str(C.calculAngle(25, 7)))
    # print( str(C.changeCoordinate(-10, 10))) 
    # print( str(C.changeCoordinate(10, 10))) 
    C.detect_distance()


