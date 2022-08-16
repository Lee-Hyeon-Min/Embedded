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


# Create your objects here.
ev3 = EV3Brick()
left_motor = Motor(Port.B) #왼쪽모터 B포트 모터 초기화
right_motor = Motor(Port.D) #오른쪽 모터 D포트 모터 초기화
h1 = HuskyLens(Port.S1,debug = False)
robot = DriveBase(left_motor, right_motor,55.5,104) #드라이브베이스 초기화

ultra = UltrasonicSensor(Port.S2)

left_cs = ColorSensor(Port.S3) #왼쪽 컬러센서 초기화
right_cs = ColorSensor(Port.S4) #오른쪽 컬러센서 초기화

black = 8
white = 63
th = (black + white) / 2
gain = 1.2

grab_motor = Motor(Port.A)

# Write your program here.

# 여기는 함수를 적는 라인
def Go_to_RED():
    while left_cs.color() != Color.RED:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(200,rate)

def Go_to_BLUE():
    while left_cs.color() != Color.BLUE:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(200,rate)


def Grab_Object():    #물체를 인식하여 집어드는 함수
    while True:
        blocks = h1.get_blocks()
        if len(blocks) > 0:
            ID = blocks[0].ID
            wait(500)
            if ID == 1:
                ev3.speaker.beep()
                robot.straight(50)
                grab_motor.run_until_stalled(200,then = Stop.COAST,duty_limit = 50)
                break
            elif ID == 2:
                ev3.speaker.beep()
                ev3.speaker.beep()
                grab_motor.run_until_stalled(200,then = Stop.COAST,duty_limit = 50)
                break
            else:
                pass
            wait(500)
    return ID

def Move_One_Block():
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)

    while right_cs.color() == Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.stop()

#여기서 부터 동작에 관여 하는 라인

grab_motor.run_until_stalled(-200, then = Stop.COAST,duty_limit = 50)

while ultra.distance() != 20:
    Move_One_Block()
    if ultra.distance() < 20:
        robot.stop()
        break
    else:
        pass
    Grab_Object()
    robot.turn(180)
    break
