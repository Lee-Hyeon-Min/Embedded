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
def Start():
    robot.straight(160)

def Go_Home():
    robot.turn(-90)
    robot.straight(100)
    
    #물체를 인식하여 집어드는 함수
def Grab_Object():
    while True:
        blocks = h1.get_blocks()
        if len(blocks) > 0:
            ID = blocks[0].ID
            wait(500)
            if ID == 1:
                ev3.speaker.beep()
                robot.straight(330)
                grab_motor.run_until_stalled(200,then = Stop.COAST,duty_limit = 50)
                break
            elif ID == 2:
                ev3.speaker.beep()
                wait(10)
                ev3.speaker.beep()
                grab_motor.run_until_stalled(200,then = Stop.COAST,duty_limit = 50)
                break
            else:
                pass
            wait(500)
    return ID



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
    robot.straight(70)
    grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)

def Go_to_Blue():
    while left_cs.color() != Color.BLACK:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(200,rate)
    robot.straight(47)
    robot.turn(-90)

    while right_cs.color() != Color.BLACK:
        rate = gain * (left_cs.reflection()-th)
        robot.drive(200, rate)
    
    while right_cs.color() == Color.BLACK:
        rate = gain * (left_cs.reflection()-th)
        robot.drive(200, rate)
    
    while right_cs.color() != Color.BLACK:
        rate = gain * (left_cs.reflection()-th)
        robot.drive(200, rate)
    robot.straight(47)
    robot.turn(100)

    while left_cs.color() != Color.BLUE:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(200,rate)
    robot.straight(50)

def Red_End(): # 빨간색에 놓고 뒤로 돌아 90도 회전 이후 출발지점으로 간다
    robot.straight(-70)
    robot.turn(190)
    while right_cs.color() != Color.BLACK:
        rate = gain * (left_cs.reflection()-th)
        robot.drive(200,rate)
    robot.straight(47)
    robot.turn(-82)
    while right_cs.color() != Color.BLACK:
        rate = gain * (left_cs.reflection()-th)
        robot.drive(200,rate)
    robot.straight(30)
    robot.turn(90)

def Blue_End(): # 파란색에 놓고 뒤로 돌아 90도 회전 이후 출발지점으로 간다
    robot.straight(-50)
    robot.turn(190)
    while left_cs.color() != Color.BLACK:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(200,rate)
    robot.straight(47)
    robot.turn(-90)
    while left_cs.color() != Color.BLACK:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(200,rate)
    
    while left_cs.color() == Color.BLACK:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(200,rate)
    
    while left_cs.color() != Color.BLACK:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(200,rate)
    
    robot.straight(40)
    robot.turn(90)

def White_Area(): #흰색 지역(4번 라인)에서 물체 찾기 (성공?)
    if ultra.distance() < 300:
        robot.straight(200)
        Grab_Object()
    else:
       Turning_For_Seeking_Object_in_White_zone()
 

def Move_One_Block_Forward_Right_Plus():
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    while right_cs.color() == Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.stop()


def Move_One_Block_Forward_Right_Minus():
    while right_cs.color() != Color.BLACK :
        rate= gain * -(left_cs.reflection() - th)
        robot.drive(200,rate)
    while right_cs.color() == Color.BLACK :
        rate= gain * -(left_cs.reflection() - th)
        robot.drive(200,rate)
    robot.stop()

def Move_One_Block_Forward_Left_Plus():
    while left_cs.color() != Color.BLACK :
        rate= gain * (right_cs.reflection() - th)
        robot.drive(200,rate)

    while left_cs.color() == Color.BLACK :
        rate= gain * (right_cs.reflection() - th)
        robot.drive(200,rate)
    robot.stop()

def Move_One_Block_Forward_Left_Minus():
    while left_cs.color() != Color.BLACK :
        rate= gain * -(right_cs.reflection() - th)
        robot.drive(200,rate)

    while left_cs.color() == Color.BLACK :
        rate= gain * -(right_cs.reflection() - th)
        robot.drive(200,rate)
    robot.stop()

def Turning_For_Seeking_Object_in_White_zone():#90도 회전하여 4번 옆의 라인에 있는 물체 찾기(성공?)
    wait(500)
    robot.turn(-90)
    if ultra.distance() < 300:
        robot.straight(300)

    elif ultra.distance() < 150:
        robot.straight(160)
    else:
        robot.turn(-90)
        Move_One_Block_Forward_Right_Plus()
        Move_One_Block_Forward_Right_Plus()
        Move_One_Block_Forward_Right_Plus()



def Turning_For_Seeking_Object_in_Black_zone():#90도 회전하여 1,2,3 옆의 라인에 있는 물체 찾기(성공?)
    robot.straight(40)
    robot.turn(108)
    if ultra.distance() < 400:
        ev3.speaker.beep()
        robot.straight(200)
        Grab_Object()
        
    elif ultra.distance() < 800:
        ev3.speaker.beep()
        Move_One_Block_Forward_Left_Minus()
        robot.straight(200)
        Grab_Object()

    else:
        robot.turn(-90)


# 여기서부터 시작
grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)
Start()




#여기는 메모 라인
"""
White_Area() 함수 확인해보기(특히 이 함수는 좀 손 많이 볼 필요 있음)
-> 이쪽은 인터넷 찾아보면서 확인해보기
Turning_For_Seeking_Object_in_Black_zone() 함수 확인해보기
Turning_For_Seeking_Object_in_White_zone() 함수 확인해보기

함수내에 함수 넣어보면서 오류 찾아보기
함수들 조합해서 원하는 결과 만들어보기
Gain 값, Threshold값에 따른 Move_One_Block 조절 



여기서 부터는 번호(159 2610 3711 4812)순서로 가는것
1번 라인만 확인해보기

여기는 1번
Move_One_Block_Forward_Right_Plus()
Grab_Object()
robot.turn(200)
Go_to_Red()
Red_End()


여기는 5번

Move_One_Block_Forward_Right_Plus()
Turning_For_Seeking_Object_in_Black_Zone()
robot.turn(200)
Move_One_Block_Forward_Left_Minus()
robot.turn(-90)
robot.straight(40)
Go_to_Red()
Red_End()


여기는 9번

Move_One_Block_Forward_Right_Plus()

Turning_For_Seeking_Object_in_Black_zone()

robot.turn(200)
Move_One_Block_Forward_Left_Minus()
Move_One_Block_Forward_Left_Minus()

robot.turn(-90)
robot.straight(40)
Go_to_Red()
Red_End()


여기는 2번
Move_One_Block_Forward_Right_Plus()
robot.straight(200)
Grab.Object()
robot.turn(200)
Move_One_Block_Left_Minus()
Go_to_Red()
Red_End()


여기는 6번
Move_One_Block_Forward_Right_Plus()
robot.turn(90)
robot.straight(200)
Grab.Object()
robot.turn(200)
Move_One_Block_Left_Minus()
robot.turn(-90)
robot.straight(40)
Move_One_Block_Left_Minus()

Go_to_Red()
Red_End()

여기는 10번
Move_One_Block_Forward_Right_Plus()
robot.turn(90)
Move_One_Block_Right_Plus()
robot.straight(200)
Grab.Object()
robot.turn(200)
Move_One_Block_Left_Minus()
robot.turn(-90)
robot.straight(40)
Move_One_Block_Left_Minus()

Go_to_Red()
Red_End()


여기는 3번
Move_One_Block_Forward_Right_Plus()
Move_One_Block_Forward_Right_Plus()
robot.straight(200)
Grab.Object()
robot.turn(200)
Move_One_Block_Left_Minus()
Go_to_Red()
Red_End()


여기는 7번
Move_One_Block_Forward_Right_Plus()
Move_One_Block_Forward_Right_Plus()
robot.turn(90)
robot.straight(200)
Grab.Object()
robot.turn(200)
Move_One_Block_Left_Minus()
robot.turn(-90)
robot.straight(40)
Move_One_Block_Left_Minus()
Move_One_Block_Left_Minus()

Go_to_Red()
Red_End()


여기는 11번
Move_One_Block_Forward_Right_Plus()
Move_One_Block_Forward_Right_Plus()

robot.turn(90)
Move_One_Block_Forward_Right_Plus()
robot.straight(200)
Grab.Object()
robot.turn(200)
Move_One_Block_Left_Minus()
robot.turn(-90)
robot.straight(40)
Move_One_Block_Left_Minus()
Move_One_Block_Left_Minus()

Go_to_Red()
Red_End()



#######################
여기 구간은 조합 구간
While True:
    Grab_Object()
    if ID == 1:
        Go_to_Red()
        Red_End()
    elif ID == 2:
        Go_to_Blue()
        Blue_End()
    else:
        Move_One_Block()
        


"""