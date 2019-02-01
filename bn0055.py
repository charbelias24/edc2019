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



while True:
    
    print('Quaternion: {}'.format(sensor.quaternion))
    q = sensor.quaternion
    ypr = get_yaw_pitch_roll(q[0],q[1],q[2],q[3])
    print('Yaw: ', ypr[0]*60)
    print('Pitch: ', ypr[1])
    print('Roll: ', ypr[2])
    time.sleep(1)

