#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
grab_motor = Motor(Port.A)

left_motor = Motor(Port.B)
right_motor = Motor(Port.D)

left_cs = ColorSensor(Port.S3)
right_cs = ColorSensor(Port.S4)

h1 = HuskyLens(Port.S1, debug=False)
us = UltrasonicSensor(Port.S2)

# Write your program here.
ev3.speaker.beep()

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

while right_cs.color()!= Color.White() & left_cs.color() != Color.White:
    robot.straight()
grab_motor.run_until_stalled(-200, then = Stop.COAST, duty_limit=50) #팔을 벌린다


