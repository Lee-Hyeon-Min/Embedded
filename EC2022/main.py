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
gain = 1.1

grab_motor = Motor(Port.A)

# Write your program here.

# 여기는 함수를 적는 라인
#def Start():
#    robot.straight(427)

def Go_to_Red():  #원점(1번)에서 빨간색으로 출발
    while left_cs.color() != Color.BLACK:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(200,rate)
    robot.straight(47)
    robot.turn(-90)
    
    while right_cs.color() != Color.BLACK:
        rate = gain * (left_cs.reflection()-th)
        robot.drive(200, rate)
    robot.straight(47)
    robot.turn(90)
    while left_cs.color() != Color.RED:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(200,rate)
    robot.straight(50)

def Red_End(): # 빨간색에 놓고 뒤로 돌아 90도 회전 이후 출발지점으로 간다
    robot.straight(-50)
    robot.turn(200)
    while right_cs.color() != Color.BLACK:
        rate = gain * (left_cs.reflection()-th)
        robot.drive(200,rate)
    
    robot.turn(100)
    while right_cs.color() != Color.BLACK:
        rate = gain * -(left_cs.reflection()-th)
        robot.drive(200,rate)
    robot.turn(90)

def Blue_End(): # 파란색에 놓고 뒤로 돌아 90도 회전 이후 출발지점으로 간다
    robot.straight(-300)
    robot.turn(100)
    while left_cs.color() != Color.BLACK:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(200,rate)
    while left_cs.color() == Color.BLACK:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(200,rate)
    while left_cs.color() != Color.BLACK:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(200,rate)
    while left_cs.color() == Color.BLACK:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(200,rate)
    robot.turn(107)

def White_Area(): #흰색 지역(4번 라인)에서 물체 찾기 (성공?)
    if ultra.distance() < 300:
        robot.straight(200)
        Grab_Object()
    else:
       Turning_For_Seeking_Object_in_White_zone()
 
def Turning_For_Seeking_Object_in_White_zone():#90도 회전하여 4번 옆의 라인에 있는 물체 찾기(성공?)
    wait(500)
    robot.turn(-90)
    if ultra.distance() < 300:
        robot.straight(300)
        Grab_Object()
    elif ultra.distance() < 150:
        robot.straight(150)
        Grab_Object()
    else:
        robot.turn(-90)
        Move_One_Block_Forward()
        Move_One_Block_Forward()
        Move_One_Block_Forward()



def Turning_For_Seeking_Object_in_Black_zone():#90도 회전하여 1,2,3 옆의 라인에 있는 물체 찾기(성공?)
    wait(500)
    robot.turn(-90)
    if ultra.distance() < 300:
        Move_One_Block_Forward()
        Move_One_Block_Forward()
        Grab_Object()
    elif ultra.distance() < 150:
        Move_One_Block_Forward()
        Grab_Object()
    else:
        robot.turn(90)
        Move_One_Block_Forward()

def Grab_Object():    #물체를 인식하여 집어드는 함수
    while True:
        blocks = h1.get_blocks()
        if len(blocks) > 0:
            ID = blocks[0].ID
            wait(500)
            if ID == 1:
                ev3.speaker.beep()
                robot.straight(150)
                grab_motor.run_until_stalled(200,then = Stop.COAST,duty_limit = 50)
                break
            elif ID == 2:
                ev3.speaker.beep()
                wait(10)
                ev3.speaker.beep()
                robot.straight(100)
                grab_motor.run_until_stalled(200,then = Stop.COAST,duty_limit = 50)
                break
            else:
                pass
            wait(500)
    return ID

def Move_One_Block_Forward():
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)

    while right_cs.color() == Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.stop()

#여기서 부터 동작에 관여 하는 라인
grab_motor.run_until_stalled(-200, then = Stop.COAST,duty_limit = 50)
Go_to_Red()
Red_End()
#Start()


#여기는 메모 라인
"""
Grab_Object() 함수 내에 Go_to_Red()와 Red_End()등의 함수 넣어보기
White_Area() 함수 확인해보기(특히 이 함수는 좀 손 많이 볼 필요 있음)
-> 이쪽은 인터넷 찾아보면서 확인해보기
Turning_For_Seeking_Object_in_Black_zone() 함수 확인해보기
Turning_For_Seeking_Object_in_White_zone() 함수 확인해보기

함수내에 함수 넣어보면서 오류 찾아보기
함수들 조합해서 원하는 결과 만들어보기
Gain 값, Threshold값에 따른 Move_One_Block 조절 
"""
