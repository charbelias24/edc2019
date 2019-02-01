import RPi.GPIO as GPIO
import time

a=1

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

def forward():
    print ("Forward")
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

def stop():
    print ("Stop")
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    GPIO.output(leftA, 0)
    GPIO.output(leftB, 0)
    GPIO.output(rightA, 0)
    GPIO.output(rightB, 0)

def clockwise():
    print ("Clockwise")
    GPIO.output(leftA, 1)
    GPIO.output(leftB, 0)
    GPIO.output(rightA, 0)
    GPIO.output(rightB, 1)

def counterClockwise():
    print ("CounterClockwise")
    GPIO.output(leftA, 0)
    GPIO.output(leftB, 1)
    GPIO.output(rightA, 1)
    GPIO.output(rightB, 0)

def shift_left():
    print ("Shift left")
    p1.ChangeDutyCycle(100)
    p2.ChangeDutyCycle(100)
    GPIO.output(leftA, 1)
    GPIO.output(leftB, 1)
    GPIO.output(rightA, 0)
    GPIO.output(rightB, 0)

def shift_right():
    print ("Shift right")
    p1.ChangeDutyCycle(100)
    p2.ChangeDutyCycle(100)
    GPIO.output(leftA, 1)
    GPIO.output(leftB, 1)
    GPIO.output(rightA, 0)
    GPIO.output(rightB, 0)

q = [forward]*a

def move(angle):
    global q
    if (80 < angle < 100):
        q.append(forward)
    elif 20 <= angle <= 80:
        q.append(shift_left)
    elif 100 <= angle <= 160:
        q.append(shift_right)
    else:
        q.append(stop)
    q.pop(0)()


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



