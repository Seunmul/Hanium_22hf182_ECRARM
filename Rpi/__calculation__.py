import math
# import matplotlib.pyplot as plt
import numpy as np
import board
import busio
import adafruit_vl53l0x

class CALCUL :
    CHECK_DIS = 5.1
    HEIGHT= 8

    def __init__(self):
        self.i2c = busio.I2C(board.SCL0, board.SDA0)
        self.vl53 = adafruit_vl53l0x.VL53L0X(self.i2c)
        pass

    def detect_distance(self) :
        while(True) :
            print(" << return distance >> ")
            # yield self.vl53.range*0.1
            # yield self.vl53*0.1
        # dis_list = []
        # print('detecting distance')
        # for _ in range(5) :
            # distance = self.vl53.range*0.1
            # dis_list.append(distance)
            # print("Range: {0}cm".format(distance))
        # dis_list.sort()
        # total = dis_list[1:-1]
        # print(sum(total)/len(total))
        # return sum(total)/len(total)
        # return self.vl53.range*0.1

    def changeCoordinate(self,x,y):
        # y = y* 1.06
        #dir = 1
        #csr = 163.2 + 25.5*(1-y)
        #n = 36*x-18
        #if n < 0:
        #    dir = 0
        #n=abs(n)    
            
        #b=2*csr*math.cos(((90-0.19*n)*math.pi)/180)
        #a=18+25.5*y
        #C=(90+0.19*n)*(math.pi)/(180)
        #c=math.sqrt(a**2+b**2-2*a*b*math.cos(C))
        #B=math.acos((c**2+a**2-b**2)/(2*a*c))
        #print(n,a,b,c,C,B*180/math.pi)
     
        #if n == 0:
        #   R = a
        #   theta = 0
        #else:
        #    R = c
        #    theta = (B*180)/math.pi
        #if dir == 1:
        #    theta = -theta

        #print('theta : ' + str(theta))
        #print('R : '+str(R))
        # x = 19.25-38.5*x
        x = 12.5-25*x
        y = 25*y
        H = 9

        y=y+H
        R = math.sqrt(x**2+y**2)
        theta = math.tan(x/y) if x != 0 else 0
        theta = math.degrees(theta)
        return R , theta

    def calculAngle(self, px, py):
        a1=17
        a2=18
        print(px,type(px))
        print(py,type(py))
        print(((((a1 + a2)**2) - (px**2 + py**2))/((px**2 + py**2)-((a1 - a2)**2))))
        temp = math.sqrt(((((a1 + a2)**2) - (px**2 + py**2))/((px**2 + py**2)-((a1 - a2)**2))))
        print(temp,type(temp))
        rsul2 = (2*math.atan(temp)) # calculate theta2
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
        height = height - 0.2
        return height
        

if __name__ == '__main__':
    C = CALCUL()
    # print( str(C.calculAngle(25, 7)))
    # print( str(C.changeCoordinate(-10, 10))) 
    # print( str(C.changeCoordinate(10, 10))) 
    C.calculAngle(10,10)
    distance=C.detect_distance()
    print(next(distance))


