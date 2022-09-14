import math
import VL53L0X
# VL53L0X.detect_distance() 거리 5번 받아와서 평균 계산


def changeCoordinate(x,y):
    H = 10
    y = y + H         ## (0,0)을 중앙 하단으로 변경 

    R = math.sqrt(math.pow(abs(x),2)+math.pow((y),2))
    theta = math.cos(y/R) if x>0  else -math.cos(y/R)
    return R , theta

# trial and error 상당히 필요함
def inverseKinematics_2(R, height=7.7) :
    ROB_1 ,ROB_2  = 16, 17

    cos = ( math.pow(R,2) + math.pow(height,2) - math.pow(ROB_1,2) - math.pow(ROB_2,2) ) / (2*ROB_1*ROB_2)
    sin = math.sqrt(1-math.pow(cos,2))

    theta2 = math.atan2(sin,cos) 
    theta1 = math.atan2(height, R) - math.atan2(ROB_1+ROB_2*math.cos(theta2),ROB_2*math.sin(theta2))
    
    theta1 = math.degrees(theta1)
    theta2 = math.degrees(theta2)
    print(str(theta1) +"   "+ str(theta2))

    return theta1,theta2

def keepVertical():
    ## 자이로 센서 받아오게
    # https://github.com/m-rtijn/mpu6050/blob/master/mpu6050/mpu6050.py
    pass