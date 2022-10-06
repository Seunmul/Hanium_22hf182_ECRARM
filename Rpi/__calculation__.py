import math
# import matplotlib.pyplot as plt
import numpy as np

import board
import busio
import adafruit_vl53l0x

class CALCUL :
    CHECK_DIS = 5.1
    HEIGHT= 13

    def __init__(self):
        self.i2c = busio.I2C(board.SCL0, board.SDA0)
        self.vl53 = adafruit_vl53l0x.VL53L0X(self.i2c)
        pass

    def detect_distance(self) :
        dis_list = []
        
        for _ in range(5) :
            distance = self.vl53.range*0.1
            dis_list.append(distance)
            # print("Range: {0}cm".format(distance))

        dis_list.sort()
        total = dis_list[1:-1]
        
        print(sum(total)/len(total))

        return sum(total)/len(total)

    def changeCoordinate(self,x,y):
        H = 20
        ## (0,0)을 중앙 하단으로 변경 
        y = y + H     
        R = math.sqrt(x**2+y**2)
        theta = math.tan(x/y) if x != 0 else 0
        theta = math.degrees(theta)
        return R , theta

    def calculAngle(self, px, py):
        a1=17; a2=18
        rsul2 = (2*math.atan((math.sqrt(((((a1 + a2)**2) - (px**2 + py**2))/((px**2 + py**2)-((a1 - a2)**2))))))) # calculate theta2
        if rsul2 < 0: # if theta2 is negative
            theta2 = rsul2 # set theta2 to negative
        else: # if theta2 is positive
            theta2 = -rsul2 # set theta2 to positive

        theta1 = math.atan(py/px ) - math.atan(((a2*math.sin(theta2))/(a1 + a2*math.cos(theta2)))) # calculate theta1

        # print("theta1:",math.degrees(theta1),"\n"+"theta2:", math.degrees(theta2)) # print theta1 and theta2

        # x1 = a1*math.cos(theta1) # calculate x1
        # y1 = a1*math.sin(theta1) # calculate y1
        # x2 = x1 + a2*math.cos(theta1+theta2) # calculate x2
        # y2 = y1 + a2*math.sin(theta1+theta2) # calculate y2

        # plt.xlim(-30, 50) # set x axis limit
        # plt.ylim(-30, 50) # set y axis limit
        # plt.plot([0, x1, x2], [0, y1, y2], 'ro-') # plot the arm
        # print("x1 = ", x1, "\ny1 = ", y1, "\nx2 = ", x2, "\ny2 = ", y2) # print x1, y1, x2, y2
        # plt.plot(px, py, 'bo') # plot the point
        # plt.show() # plot

        theta1 = theta1*180/math.pi
        theta2 = theta2*180/math.pi 
        
        # print("1" + str(theta1) + " " + str(theta2))

        theta3 = abs( theta1 + theta2 )
        theta2 = theta2 + 90

        # print("2" + str(theta1) + " " + str(theta2)+ " " + str(theta3))
        return theta1, theta2, theta3

    def decreaseDis(self, height) :
        height = height - 0.3
        return height
        

if __name__ == '__main__':
    C = CALCUL()
    # print( str(C.calculAngle(25, 7)))
    # print( str(C.changeCoordinate(-10, 10))) 
    # print( str(C.changeCoordinate(10, 10))) 
    C.calculAngle(10,10)


