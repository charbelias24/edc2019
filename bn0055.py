import time
import board
import busio
import adafruit_bno055
import math
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055(i2c, 0x29)

def get_yaw_pitch_roll(x,y,z,w):
    yaw = math.atan2(2.0*(y*z + w*x), w*w - x*x - y*y + z*z);
    pitch = math.asin(-2.0*(x*z - w*y));
    roll = math.atan2(2.0*(x*y + w*z), w*w + x*x - y*y - z*z);
    return yaw, pitch, roll

def get_yaw(x,y,z,w):
     return math.atan2(2.0*(y*z + w*x), w*w - x*x - y*y + z*z) + 180



def turn():
    initial = get_yaw(sensor.quaternion)
    done = False
    stop = False
    while((not stop) and (not done)):
        current = math.abs(get_yaw(sensor.quaternion) - initial)
        print('Current absolute yaw diff: ', current)
        if(current >= 90):
            done = True
            print('Done turning')
    

