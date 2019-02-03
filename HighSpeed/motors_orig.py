import RPi.GPIO as GPIO
import time
#import board
#import busio
#import adafruit_bno055
import math

#i2c = busio.I2C(board.SCL, board.SDA)
#sensor = adafruit_bno055.BNO055(i2c, 0x29)

a = 2

leftA = 8
leftB = 10

rightA = 12
rightB = 16

trig = 3
echo = 5

red = 7
green = 18

enableA = 40
enableB = 38

GPIO.setmode(GPIO.BOARD)

GPIO.setup(leftA, GPIO.OUT)
GPIO.setup(leftB, GPIO.OUT)

GPIO.setup(rightA, GPIO.OUT)
GPIO.setup(rightB, GPIO.OUT)

GPIO.setup(enableA, GPIO.OUT)
GPIO.setup(enableB, GPIO.OUT)

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)

GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

p1 = GPIO.PWM(enableA, 100)
p2 = GPIO.PWM(enableB, 100)

p1.start(100)
p2.start(100)

stop = False

def get_yaw(q):
     return math.atan2(2.0*(q[1]*q[2] + q[3]*q[0]), q[3]*q[3] - q[0]*q[0]
                       - q[1]*q[1] + q[2]*q[2]) + 180
    
def turn():

    pass
    '''initial = get_yaw(sensor.quaternion)
    done = False
    stop = False
    while((not stop) and (not done)):
        current = math.abs(get_yaw(sensor.quaternion) - initial)
        print('Current absolute yaw diff: ', current)
        if(current >= 90):
            done = True
            print('Done turning')'''
    

def forward(angle):
    print ("Forwrd")
    p1.ChangeDutyCycle(100)
    p2.ChangeDutyCycle(100)

    GPIO.output(leftA, 1)
    GPIO.output(leftB, 1)
    GPIO.output(rightA, 0)
    GPIO.output(rightB, 0)

def backward():
    print ("Backward")
    p1.ChangeDutyCycle(30)
    p2.ChangeDutyCycle(30)
    GPIO.output(leftA, 0)
    GPIO.output(leftB, 0)
    GPIO.output(rightA, 1)
    GPIO.output(rightB, 1)

def stop(angle):
    print ("Stop")
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    GPIO.output(leftA, 1)
    GPIO.output(leftB, 1)
    GPIO.output(rightA, 1)
    GPIO.output(rightB, 1)

def clockwise():
    print ("Clockwise")
    p1.ChangeDutyCycle(80)
    p2.ChangeDutyCycle(80)
    GPIO.output(leftA, 1)
    GPIO.output(leftB, 0)
    GPIO.output(rightA, 0)
    GPIO.output(rightB, 1)

def counterClockwise():
    print ("CounterClockwise")
    p1.ChangeDutyCycle(80)
    p2.ChangeDutyCycle(80)
    GPIO.output(leftA, 0)
    GPIO.output(leftB, 1)
    GPIO.output(rightA, 1)
    GPIO.output(rightB, 0)

def shift_left(angle):
    print ("Shift left")
    
    speed = (180 - angle)
    speed = 0 if speed < 30 else speed
    print (speed / 4, 100)
    p1.ChangeDutyCycle(speed)
    p2.ChangeDutyCycle(100)
    
    if angle < 130:
   	GPIO.output(leftA, 1)
    	GPIO.output(leftB, 1)
    	GPIO.output(rightA, 0)
    	GPIO.output(rightB, 0)
    else:
        print ('+'*100)
        p1.ChangeDutyCycle(speed / 1.126) 
   	GPIO.output(leftA, 1)
    	GPIO.output(leftB, 1)
    	GPIO.output(rightA, 1)
    	GPIO.output(rightB, 0)
##    turn()
##    forward()

def shift_right(angle):

    print ("Shift right")
    speed = angle
    speed = 0 if speed < 30 else speed
    print (100, speed / 4)
    p1.ChangeDutyCycle(100)
    p2.ChangeDutyCycle(speed)
    if angle > 50:
        GPIO.output(leftA, 1)
        GPIO.output(leftB, 1)
        GPIO.output(rightA, 0)
        GPIO.output(rightB, 0)
    else:
        print ('-----------------------------')
        p2.ChangeDutyCycle(speed / 1.126)
        GPIO.output(leftA, 1)
        GPIO.output(leftB, 0)
        GPIO.output(rightA, 0)
        GPIO.output(rightB, 0)
##    turn()
##    forward()

q = [(forward,90)]*a

def move(angle):
    global q
    print (angle)
    if (70 < angle < 110):
        q.append((forward, angle))
    elif 0 < angle <= 70:
        q.append((shift_right,angle))
    elif 110 <= angle < 180:
        q.append((shift_left, angle))
    else:
        q.append((stop, angle))
    temp = q.pop(0)
    temp[0](temp[1])

def exit_m():
    stop()
    p1.stop()
    p2.stop()


def ultrasonic(trig, echo):
        GPIO.output(trig, True)
        time.sleep(0.00001)
        GPIO.output(trig, False)
        while GPIO.input(echo) == 0:
            start = time.time()
        while GPIO.input(echo) == 1:
            stop = time.time()
        timePassed = stop-start
        distance = timePassed * 17000
        distance = round(distance, 2)
        print ('Distance:', distance, 'cm')
        return distance
        time.sleep(0.5)



