import i2c0_lidar
import time

while True: 
    dis = i2c0_lidar.detect_distance()
    print(dis , "mm\n")
    time.sleep(1)
