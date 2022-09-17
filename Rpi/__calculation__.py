import math
import board
import busio
import adafruit_vl53l0x

class CALCUL :
    CHECK_DIS = 1
    HEIGHT=7.7

    def __init__(self):
        self.i2c = busio.I2C(board.SCL0, board.SDA0)
        self.vl53 = adafruit_vl53l0x.VL53L0X(i2c)
        pass

    def detect_distance(self) :
        sum = 0
        for _ in range(5) :
            distance = self.vl53.range
            sum += distance
            print("Range: {0}mm".format(distance))
        
        # VL53L0X.detect_distance() 거리 5번 받아와서 평균 계산
        return sum/5 

    def changeCoordinate(self,x,y):
        H = 10
        ## (0,0)을 중앙 하단으로 변경 
        y = y + H     

        R = math.sqrt(math.pow(abs(x),2)+math.pow((y),2))
        theta = math.cos(y/R) if x>0  else -math.cos(y/R)
        theta = math.degrees(theta)
        return R , theta

    # trial and error 상당히 필요함
    def calculAngle(self, R, HEIGHT) :
        ROB_1 ,ROB_2  = 16, 17

        cos = ( math.pow(R,2) + math.pow(HEIGHT,2) - math.pow(ROB_1,2) - math.pow(ROB_2,2) ) / (2*ROB_1*ROB_2)
        sin = - math.sqrt(1-math.pow(cos,2))

        theta2 = math.atan2(sin,cos) 
        theta1 = math.atan2(HEIGHT, R) - math.atan2(ROB_1+ROB_2*math.cos(theta2),ROB_2*math.sin(theta2))
        
        theta1 = math.degrees(theta1)
        theta2 = math.degrees(theta2)
        theta2 = theta2 + 90 # theta2 가 음수라는 가정
        theta3 = self.keepVertical(theta1, theta2)

        return theta1,theta2, theta3

    def keepVertical(self, theta1, theta2):
        return theta1+theta2

    def classification(self, element) :
        pass     