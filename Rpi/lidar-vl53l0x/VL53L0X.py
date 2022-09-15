import board
import busio
import adafruit_vl53l0x

i2c = busio.I2C(board.SCL0, board.SDA0)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

def detect_distance() :
    sum = 0
    for _ in range(5) :
        distance = vl53.range
        sum += distance
        print("Range: {0}mm".format(distance))
    
    return sum/5 