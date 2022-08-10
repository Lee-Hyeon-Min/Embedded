#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

from pyhuskylens import *
# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# Create your objects here.ev3 = EV3Brick()
ev3 = EV3Brick()
grab_motor = Motor(Port.A)

left_motor = Motor(Port.B)
right_motor = Motor(Port.D)

left_cs = ColorSensor(Port.S3)
right_cs = ColorSensor(Port.S4)

h1 = HuskyLens(Port.S1, debug=False)
us = UltrasonicSensor(Port.S2)
# Write your program here.

robot = DriveBase(left_motor, right_motor, 55.4, 104)
# while True:
#     if cs.color() == Color.BLACK:
#         robot.drive(100, -20)
#     else:
#         robot.drive(100, 20)

# 조향값 설정
black = 8
white = 62
th = (black + white) / 2
# while True:
#     rate = gain * (cs.reflection() - th)
#     robot.drive(150, turn_rate)
#     wait(10)
# 반사광 - th
# 80 -45 = 35 조향값
# 10 -45 = -35 조향값


gain= 0.8
### 1번
grab_motor.run_until_stalled(-200, then = Stop.COAST, duty_limit=50)

while right_cs.color() != Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)

while right_cs.color() == Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)

robot.stop()
while True:
    blocks = h1.get_blocks()
    if len(blocks) > 0:
        ID = blocks[0].ID
        wait(500)
        if ID == 1:
            a = 1
            ev3.speaker.beep()
            break
        elif ID == 2:
            ev3.speaker.beep()
            ev3.speaker.beep()
            a = 2
            break
        else:
            a = 0
            pass
        print(a)
    else:
        print('계속')
    wait(500)

while right_cs.color() != Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
    print(us.distance())
    if us.distance() < 56:
        robot.stop()
        break
grab_motor.run_until_stalled(200, then = Stop.COAST, duty_limit=50)
robot.turn(180)

while left_cs.color() != Color.BLACK :
    rate= gain * -(right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() == Color.BLACK :
    rate= gain * -(right_cs.reflection() - th)
    robot.drive(200,rate)

robot.straight(50)
robot.turn(-90)
if a == 1:
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn(90)

    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.stop()
    grab_motor.run_until_stalled(-200, then = Stop.COAST, duty_limit=50)

    wait(3000)

    robot.turn(180)
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn(-90)

    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn(90)

elif a == 2:
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    while right_cs.color() == Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn (90)
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.stop()
    grab_motor.run_until_stalled(-200, then = Stop.COAST, duty_limit=50)

    wait(3000)

    robot.turn(180)

    while left_cs.color() != Color.BLACK :
        rate= gain * -(right_cs.reflection() - th)
        robot.drive(200,rate)
    
    robot.straight(30)
    robot.turn(-100)

    while left_cs.color() != Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    while left_cs.color() == Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    while left_cs.color() != Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    while left_cs.color() == Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    robot.turn(90)

#### 2번
while right_cs.color() != Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
while right_cs.color() == Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
robot.stop()

while True:
    blocks = h1.get_blocks()
    if len(blocks) > 0:
        ID = blocks[0].ID
        wait(500)
        if ID == 1:
            a = 1
            ev3.speaker.beep()
            break
        elif ID == 2:
            ev3.speaker.beep()
            ev3.speaker.beep()
            a = 2
            break
        else:
            a = 0
            pass
        print(a)
    else:
        print('계속')
    wait(500)

while right_cs.color() != Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
    print(us.distance())
    if us.distance() < 56:
        robot.stop()
        break
grab_motor.run_until_stalled(200, then = Stop.COAST, duty_limit=50)
robot.turn(180)

while left_cs.color() != Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() == Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() != Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() == Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)

robot.straight(50)
robot.turn(-90)
if a == 1:
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn(90)

    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.stop()
    grab_motor.run_until_stalled(-200, then = Stop.COAST, duty_limit=50)

    wait(3000)

    robot.turn(180)
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn(-90)

    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn(90)

elif a == 2:
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    while right_cs.color() == Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn (90)
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.stop()
    grab_motor.run_until_stalled(-200, then = Stop.COAST, duty_limit=50)

    wait(3000)

    robot.turn(180)

    while left_cs.color() != Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    
    robot.straight(30)
    robot.turn(-100)

    while left_cs.color() != Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    while left_cs.color() == Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    while left_cs.color() != Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    while left_cs.color() == Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    robot.turn(90)

###3번

while right_cs.color() != Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
while right_cs.color() == Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
while right_cs.color() != Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
while right_cs.color() == Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)

robot.stop()
while True:
    blocks = h1.get_blocks()
    if len(blocks) > 0:
        ID = blocks[0].ID
        wait(500)
        if ID == 1:
            a = 1
            ev3.speaker.beep()
            break
        elif ID == 2:
            ev3.speaker.beep()
            ev3.speaker.beep()
            a = 2
            break
        else:
            a = 0
            pass
        print(a)
    else:
        print('계속')
    wait(500)

while right_cs.color() != Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
    print(us.distance())
    if us.distance() < 56:
        robot.stop()
        break
grab_motor.run_until_stalled(200, then = Stop.COAST, duty_limit=50)
robot.turn(185)

while left_cs.color() != Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() == Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() != Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() == Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() != Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() == Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)

robot.straight(50)
robot.turn(-90)
if a == 1:
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn(90)

    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.stop()
    grab_motor.run_until_stalled(-200, then = Stop.COAST, duty_limit=50)

    wait(3000)

    robot.turn(180)
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn(-90)

    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn(90)

elif a == 2:
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    while right_cs.color() == Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn (90)
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.stop()
    grab_motor.run_until_stalled(-200, then = Stop.COAST, duty_limit=50)

    wait(3000)

    robot.turn(180)

    while left_cs.color() != Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    
    robot.straight(30)
    robot.turn(-100)

    while left_cs.color() != Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    while left_cs.color() == Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    while left_cs.color() != Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    while left_cs.color() == Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    robot.turn(90)

### 5번
while right_cs.color() != Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
while right_cs.color() == Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
robot.stop()
robot.straight(30)
robot.turn(97)

while True:
    blocks = h1.get_blocks()
    if len(blocks) > 0:
        ID = blocks[0].ID
        wait(500)
        if ID == 1:
            a = 1
            ev3.speaker.beep()
            break
        elif ID == 2:
            ev3.speaker.beep()
            ev3.speaker.beep()
            a = 2
            break
        else:
            a = 0
            pass
        print(a)
    else:
        print('계속')
    wait(500)

while right_cs.color() != Color.BLACK :
    rate= 1.2 * gain * (left_cs.reflection() - th)
    robot.drive(100,rate)
    print(us.distance())
    if us.distance() < 56:
        robot.stop()
        robot.straight(50)
        break
grab_motor.run_until_stalled(200, then = Stop.COAST, duty_limit=50)

robot.turn(190)

robot.straight(50)

while left_cs.color() != Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() == Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)


# while right_cs.color() != Color.BLACK :
#     rate= gain * (left_cs.reflection() - th)
#     robot.drive(200,rate)
# while right_cs.color() == Color.BLACK :
#     rate= gain * (left_cs.reflection() - th)
#     robot.drive(200,rate)
robot.straight(30)
robot.turn(-90)

while left_cs.color() != Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() == Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)


robot.straight(50)
robot.turn(-90)
if a == 1:
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn(90)

    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.stop()
    grab_motor.run_until_stalled(-200, then = Stop.COAST, duty_limit=50)

    wait(3000)

    robot.turn(180)
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn(-90)

    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn(90)

elif a == 2:
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    while right_cs.color() == Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn (90)
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.stop()
    grab_motor.run_until_stalled(-200, then = Stop.COAST, duty_limit=50)

    wait(3000)

    robot.turn(180)

    while left_cs.color() != Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    
    robot.straight(30)
    robot.turn(-100)

    while left_cs.color() != Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    while left_cs.color() == Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    while left_cs.color() != Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    while left_cs.color() == Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    robot.turn(90)

### 6번
while right_cs.color() != Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
while right_cs.color() == Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
while right_cs.color() != Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
while right_cs.color() == Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
robot.stop()
robot.straight(30)
robot.turn(97)

while True:
    blocks = h1.get_blocks()
    if len(blocks) > 0:
        ID = blocks[0].ID
        wait(500)
        if ID == 1:
            a = 1
            ev3.speaker.beep()
            break
        elif ID == 2:
            ev3.speaker.beep()
            ev3.speaker.beep()
            a = 2
            break
        else:
            a = 0
            pass
        print(a)
    else:
        print('계속')
    wait(500)

while right_cs.color() != Color.BLACK :
    rate= 1.2 * gain * (left_cs.reflection() - th)
    robot.drive(100,rate)
    print(us.distance())
    if us.distance() < 56:
        robot.stop()
        robot.straight(60)
        break
grab_motor.run_until_stalled(200, then = Stop.COAST, duty_limit=50)

robot.turn(190)
robot.straight(50)

while left_cs.color() != Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() == Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
# while right_cs.color() != Color.BLACK :
#     rate= gain * (left_cs.reflection() - th)
#     robot.drive(200,rate)
# while right_cs.color() == Color.BLACK :
#     rate= gain * (left_cs.reflection() - th)
#     robot.drive(200,rate)

robot.straight(30)
robot.turn(-90)

while left_cs.color() != Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() == Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() != Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() == Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)


robot.straight(50)
robot.turn(-90)
if a == 1:
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn(90)

    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.stop()
    grab_motor.run_until_stalled(-200, then = Stop.COAST, duty_limit=50)

    wait(3000)

    robot.turn(180)
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn(-90)

    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn(90)

elif a == 2:
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    while right_cs.color() == Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn (90)
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.stop()
    grab_motor.run_until_stalled(-200, then = Stop.COAST, duty_limit=50)

    wait(3000)

    robot.turn(180)

    while left_cs.color() != Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    
    robot.straight(30)
    robot.turn(-100)

    while left_cs.color() != Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    while left_cs.color() == Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    while left_cs.color() != Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    while left_cs.color() == Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    robot.turn(90)

### 7번
while right_cs.color() != Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
while right_cs.color() == Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
while right_cs.color() != Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
while right_cs.color() == Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
while right_cs.color() != Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
while right_cs.color() == Color.BLACK :
    rate= gain * (left_cs.reflection() - th)
    robot.drive(200,rate)
robot.stop()
robot.straight(30)
robot.turn(97)

while True:
    blocks = h1.get_blocks()
    if len(blocks) > 0:
        ID = blocks[0].ID
        wait(500)
        if ID == 1:
            a = 1
            ev3.speaker.beep()
            break
        elif ID == 2:
            ev3.speaker.beep()
            ev3.speaker.beep()
            a = 2
            break
        else:
            a = 0
            pass
        print(a)
    else:
        print('계속')
    wait(500)

while right_cs.color() != Color.BLACK :
    rate= 1.2 * gain * (left_cs.reflection() - th)
    robot.drive(100,rate)
    print(us.distance())
    if us.distance() < 56:
        robot.stop()
        robot.straight(70)
        break
grab_motor.run_until_stalled(200, then = Stop.COAST, duty_limit=50)
robot.turn(190)
robot.straight(50)

while left_cs.color() != Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() == Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
# while right_cs.color() != Color.BLACK :
#     rate= gain * (left_cs.reflection() - th)
#     robot.drive(200,rate)
# while right_cs.color() == Color.BLACK :
#     rate= gain * (left_cs.reflection() - th)
#     robot.drive(200,rate)
robot.straight(30)
robot.turn(-90)

while left_cs.color() != Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() == Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() != Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() == Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() != Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() == Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)


robot.straight(50)
robot.turn(-90)
if a == 1:
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn(90)

    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.stop()
    grab_motor.run_until_stalled(-200, then = Stop.COAST, duty_limit=50)

    wait(3000)

    robot.turn(180)
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn(-90)

    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn(-90)

elif a == 2:
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    while right_cs.color() == Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.straight(50)
    robot.turn (90)
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.stop()
    grab_motor.run_until_stalled(-200, then = Stop.COAST, duty_limit=50)

    wait(3000)

    robot.turn(180)

    while left_cs.color() != Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    
    robot.straight(30)
    robot.turn(-100)

    while left_cs.color() != Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    while left_cs.color() == Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    while left_cs.color() != Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    while left_cs.color() == Color.BLACK :
        rate= -gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    robot.turn(-90)
#마무리
while left_cs.color() != Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
while left_cs.color() == Color.BLACK :
    rate= -gain * (right_cs.reflection() - th)
    robot.drive(200,rate)
robot.straight(250)
robot.stop()