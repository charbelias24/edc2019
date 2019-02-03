
import RPi.GPIO as GPIO
import time
import math


a = 1

#motors pins
leftA = 18
leftB = 10

rightA = 12
rightB = 16

enableA = 40
enableB = 38

GPIO.setmode(GPIO.BOARD)

GPIO.setup(leftA, GPIO.OUT)
GPIO.setup(leftB, GPIO.OUT)

GPIO.setup(rightA, GPIO.OUT)
GPIO.setup(rightB, GPIO.OUT)

GPIO.setup(enableA, GPIO.OUT)
GPIO.setup(enableB, GPIO.OUT)

p1 = GPIO.PWM(enableA, 100)
p2 = GPIO.PWM(enableB, 100)

p1.start(100)
p2.start(100)

#calibrating shifts
Forward_Upper_Limit = 110
Forward_Lower_Limit =70

Shift_Speed = 50
Shift_Ratio = 5
Max_Speed = 100
BrakeTorqueRatio =1
MaxBreakSpeed = 40
RightBreakAngle = 140
LeftBreakAngle =40
BreakRatio = MaxBreakSpeed/LeftBreakAngle
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

def shift_right(angle):
    print ("Shift right")
    speed = (180 - angle)
    print (speed / Shift_Ratio, 100)
    p1.ChangeDutyCycle(speed/Shift_Ratio)
    p2.ChangeDutyCycle(Max_Speed)
   
    if angle <RightBreakAngle:
         GPIO.output(leftA, 1)
         GPIO.output(leftB, 1)
         GPIO.output(rightA, 0)
         GPIO.output(rightB, 0)
    else:
        print ('+'*100)
#	breakSpeed = (angle-RightBreakAngle)*BreakRatio
        p2.ChangeDutyCycle(speed*BrakeTorqueRatio)
        p1.ChangeDutyCycle(MaxBreakSpeed)
	GPIO.output(leftA, 0)
        GPIO.output(leftB, 1)
        GPIO.output(rightA, 1)
        GPIO.output(rightB, 0)

def shift_left(angle):

    print ("Shift left")
    speed = angle
    p2.ChangeDutyCycle(speed/Shift_Ratio)
    p1.ChangeDutyCycle(Max_Speed)
   
    if angle>LeftBreakAngle:
        GPIO.output(leftA, 1)
        GPIO.output(leftB, 1)
        GPIO.output(rightA, 0)
        GPIO.output(rightB, 0)
    else:
        print ('-----------------------------')
#	breakSpeed = (angle-RightBreakAngle)*BreakRatio
        p1.ChangeDutyCycle(speed*BrakeTorqueRatio)
        p2.ChangeDutyCycle(MaxBreakSpeed)
	GPIO.output(leftA, 1)
        GPIO.output(leftB, 0)
        GPIO.output(rightA,0)
        GPIO.output(rightB, 1)


q = [(forward,90)]*a

def move(angle):
    global q
    print (angle)
    if ( Forward_Lower_Limit< angle < Forward_Upper_Limit):
        q.append((forward, angle))        
    elif 0 < angle <= Forward_Lower_Limit:
        q.append((shift_left,angle))        
    elif Forward_Upper_Limit <= angle < 180:
        q.append((shift_right, angle))        
    else:
        q.append((stop, angle))
    temp = q.pop(0)
    temp[0](temp[1])
   

def exit_m():
    stop()
    p1.stop()
    p2.stop()


'''while (1):
	testAngle=10
	while testAngle<180:
		testAngle+=10
		move(testAngle)
		time.sleep(1.56)
'''
