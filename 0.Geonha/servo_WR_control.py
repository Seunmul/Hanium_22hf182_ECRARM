import time
from threading import Thread

# import busio
# from board import SCL, SDA # Import board module info
# from adafruit_pca9685 import PCA9685  # Import the PCA9685 module.

def _DEGREE_TO_PWM_(interval, min_pwm, degree):
    pwm = min_pwm + (interval*180) if degree>180 else min_pwm + (interval*degree)
    return pwm

def _SERVO_SETUP_(MIN, MAX):
    degree_per_interval = round(float(MAX-MIN)/180,1)
    return degree_per_interval, MIN, MAX

def _SERVO_MIN_PWM_(channel_num, cur_pwm, interval):
    print("\nmin_pwm")
    while cur_pwm > min_pwm:
        cur_pwm = cur_pwm - interval if((cur_pwm-interval)>min_pwm) else min_pwm
        # pca.channels[channel_num].duty_cycle = cur_pwm
        time.sleep(0.001)
    print("stop")
    return cur_pwm

def _SERVO_MAX_PWM_(channel_num, cur_pwm, interval):
    print("\nmax_pwm")
    while cur_pwm < max_pwm:
        cur_pwm = cur_pwm + interval if((cur_pwm+interval)<max_pwm) else max_pwm
        # pca.channels[channel_num].duty_cycle = cur_pwm
        time.sleep(0.001)
    print("stop")
    return cur_pwm

def _SERVO_CONTROL_(channel_num, cur_pwms, interval, min_pwm, max_pwm, degree_pwm):
    cur_pwm=cur_pwms[channel_num]
    print("목표 pwm : %d" % (degree_pwm))
    if(cur_pwm < degree_pwm):
        while cur_pwm < degree_pwm:
            cur_pwm = cur_pwm +interval if((cur_pwm + interval)<degree_pwm) else degree_pwm
            # pca.channels[channel_num].duty_cycle = cur_pwm
            time.sleep(0.001)
    elif(cur_pwm > degree_pwm):
        while cur_pwm > degree_pwm:
            cur_pwm = cur_pwm - interval if((cur_pwm-interval)>degree_pwm) else degree_pwm
            # pca.channels[channel_num].duty_cycle = cur_pwm
            time.sleep(0.001)
    print("stop")
    # print(cur_pwm)
    cur_pwms[channel_num]=cur_pwm
    return cur_pwm

if __name__ == "__main__":
    try:
        # initialize I2C BUS with PCA9685
        # I2C_BUS = busio.I2C(SCL, SDA)  # Create the I2C bus interface.
        # pca = PCA9685(I2C_BUS)  # Create a simple PCA9685 class instance.
        # pca.frequency = 60  # Set the PWM frequency to 60hz.

        #setting servo with pca9685, and intialize motor 
        print("initializing....")
        interval, min_pwm, max_pwm = _SERVO_SETUP_(MIN=0x07f5, MAX=0x1b6f)
        print("%f %d %d" % (interval, min_pwm, max_pwm))
        cur_pwms=[0,0]
        
        cur_pwms[0] = _SERVO_MIN_PWM_(0, min_pwm, interval) 
        print(cur_pwms)
        time.sleep(0.5)
        
        cur_pwms[0] = _SERVO_MAX_PWM_(0, cur_pwms[0], interval)
        print(cur_pwms)
        time.sleep(0.5)
        
        while True:

            print(cur_pwms)
            
            degree_pwm = _DEGREE_TO_PWM_(
                interval, min_pwm, degree=int(input("각도를입력하세요 : ")))

            # cur_pwm = _SERVO_CONTROL_(
            #     0, cur_pwm, interval, min_pwm, max_pwm, degree_pwm)
            # time.sleep(0.5)
            
            ##threading test
            W_axis=Thread(name="W_axis", target=_SERVO_CONTROL_, args=(0, cur_pwms, interval, min_pwm, max_pwm, degree_pwm))
            R_axis=Thread(name="R_axis", target=_SERVO_CONTROL_, args=(1, cur_pwms, interval, min_pwm, max_pwm, degree_pwm))

            # start control thread
            W_axis.start()
            R_axis.start()
            
            # wait control thread
            W_axis.join()
            R_axis.join()
            
    except KeyboardInterrupt:
        pass
    finally :
        print("\n\ninitialize Servo...")
        for cur_pwm in cur_pwms :
            cur_pwm = _SERVO_MIN_PWM_(0, cur_pwm, interval)
        print(cur_pwm)
        print("test_end")
        # 0x1fff 10% 180 degree
        # 0x1265 7.5% 90 degree
        # 0x4cc 5% 0 degree
