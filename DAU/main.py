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


# Write your program here.
left_motor = Motor(Port.B) #왼쪽모터 B포트 모터 초기화
right_motor = Motor(Port.D) #오른쪽 모터 D포트 모터 초기화

robot = DriveBase(left_motor, right_motor,55.5,104) #드라이브베이스 초기화

ultra = UltrasonicSensor(Port.S2)

left_cs = ColorSensor(Port.S3) #왼쪽 컬러센서 초기화
right_cs = ColorSensor(Port.S4) #오른쪽 컬러센서 초기화

black = 7
white = 57
th = (black + white) / 2
drive_speed = 100
gain = 1.2

grab_motor = Motor(Port.A)

grab_motor.run_until_stalled(-200, then = Stop.COAST,duty_limit = 50)

while right_cs.color() != Color.BLACK:
    rate = gain*(left_cs.reflection()-th)
    robot.drive(100,rate)

while right_cs.color() == Color.BLACK:
    
    rate = gain*(left_cs.reflection()-th)
    robot.drive(100,rate)    
while ultra.distance() > 100:
    rate = gain*(left_cs.reflection()-th)
    robot.drive(100,rate)    
robot.stop()
robot.straight(100)
grab_motor.run_until_stalled(200, then = Stop.COAST, duty_limit = 50)

robot.turn(180)

while left_cs.color() != Color.BLACK:
    rate = -gain*(right_cs.reflection()-th)
    robot.drive(100,rate)

robot.straight(50)
robot.turn(-90)

while right_cs.color() != Color.BLACK:
    
    rate = gain*(left_cs.reflection()-th)
    robot.drive(100,rate)    

robot.straight(50)
robot.turn(90)
while right_cs.color() != Color.RED:
    
    rate = gain*(left_cs.reflection()-th)
    robot.drive(100,rate)    
robot.stop()
grab_motor.run_until_stalled(-200, then = Stop.COAST, duty_limit = 50)

robot.stop()
ev3.speaker.beep()
#wait(100)#100ms 동안 기다린다
#ev3.speaker.beep(1500,1000)#1500Hz의 주파수를 1000ms 동안 재생한다

