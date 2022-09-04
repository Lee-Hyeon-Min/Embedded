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
def Start(): # 시작한다
    robot.straight(160)

def Go_Home(): # 끝나면 집으로 간다
    robot.turn(-90)
    robot.straight(100)
    
# 물체를 인식하여 집어드는 함수
def Grab_Object():
    while True:
        blocks = h1.get_blocks()
        if len(blocks) > 0:
            global ID
            ID = blocks[0].ID
            wait(500)
            if ID == 1: #캔
                robot.straight(75)
                robot.stop()
                grab_motor.run_until_stalled(200,then = Stop.COAST,duty_limit = 50)
                break
            elif ID == 2: #패트병
                robot.straight(75)
                robot.stop()
                grab_motor.run_until_stalled(200,then = Stop.COAST,duty_limit = 50)
                break
            else:
                pass
            wait(500)
    return ID



def Go_to_Red():  # 원점(1번)에서 빨간색으로 출발
    while left_cs.color() != Color.BLACK:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(250,rate)
    robot.straight(47)
    robot.turn(-90)
    
    while right_cs.color() != Color.BLACK:
        rate = gain * (left_cs.reflection()-th)
        robot.drive(250, rate)
    robot.straight(47)
    robot.turn(90)
    while left_cs.color() != Color.RED:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(250,rate)
    robot.straight(70)
    grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)

def Go_to_Blue1(): # 원점(1번 밑)을 기준으로 Blue 가기
    while left_cs.color() != Color.BLACK:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(250,rate)
    robot.straight(47)
    robot.turn(-90)

    Move_One_Block_Forward_Right_Plus()
    
    while right_cs.color() != Color.BLACK:
        rate = gain * (left_cs.reflection()-th)
        robot.drive(250, rate)
    robot.straight(47)
    robot.turn(100)

    while left_cs.color() != Color.BLUE:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(250,rate)
    robot.straight(70)
    grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)

def Go_to_Blue2(): # 5번 기준으로 Blue 가기
    wait(500)
    robot.straight(50)
    robot.turn(90)
    robot.straight(250)
    robot.turn(-110)

    Move_One_Block_Forward_Right_Plus()

    robot.turn(90)
    while right_cs.color() != Color.BLACK:
        rate = gain * (left_cs.reflection()-th)
        robot.drive(250, rate)
    robot.straight(47)
    robot.turn(100)

    while left_cs.color() != Color.BLUE:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(250,rate)
    robot.straight(70)
    grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)


def Red_End(): # 빨간색에 놓고 뒤로 돌아 90도 회전 이후 출발지점으로 간다
    robot.straight(-90)
    robot.turn(190)
    while right_cs.color() != Color.BLACK:
        rate = gain * (left_cs.reflection()-th)
        robot.drive(250,rate)
    robot.straight(47)
    robot.turn(-82)
    while right_cs.color() != Color.BLACK:
        rate = gain * (left_cs.reflection()-th)
        robot.drive(250,rate)
    robot.straight(30)
    robot.turn(90)

    Move_One_Block_Forward_Right_Plus()

def Blue_End(): # 파란색에 놓고 뒤로 돌아 90도 회전 이후 출발지점으로 간다
    robot.straight(-90)
    robot.turn(190)
    while left_cs.color() != Color.BLACK:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(250,rate)
    robot.straight(47)
    robot.turn(-90)
    while left_cs.color() != Color.BLACK:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(250,rate)
    
    Move_One_Block_Forward_Left_Minus()
        
    robot.straight(40)
    robot.turn(90)

    Move_One_Block_Forward_Right_Plus()

def White_Area(): #흰색 지역(4번 라인)에서 물체 찾기 (성공?)
    if ultra.distance() < 300:
        robot.straight(200)
        Grab_Object()
    else:
       pass
 

def Move_One_Block_Forward_Right_Plus(): 
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(250,rate)
    while right_cs.color() == Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(250,rate)
    robot.stop()


def Move_One_Block_Forward_Right_Minus():
    while right_cs.color() != Color.BLACK :
        rate= gain * -(left_cs.reflection() - th)
        robot.drive(250,rate)
    while right_cs.color() == Color.BLACK :
        rate= gain * -(left_cs.reflection() - th)
        robot.drive(250,rate)
    robot.stop()

def Move_One_Block_Forward_Left_Plus():
    while left_cs.color() != Color.BLACK :
        rate= gain * (right_cs.reflection() - th)
        robot.drive(250,rate)

    while left_cs.color() == Color.BLACK :
        rate= gain * (right_cs.reflection() - th)
        robot.drive(250,rate)
    robot.stop()

def Move_One_Block_Forward_Left_Minus():
    while left_cs.color() != Color.BLACK :
        rate= gain * -(right_cs.reflection() - th)
        robot.drive(250,rate)

    while left_cs.color() == Color.BLACK :
        rate= gain * -(right_cs.reflection() - th)
        robot.drive(250,rate)
    robot.stop()

def Turning_For_Seeking_Object_in_White_Zone():# 90도 회전하여 4번 옆의 라인에 있는 물체 찾기(성공?)
    wait(500)
    robot.turn(90)
    if ultra.distance() < 300:
        robot.straight(300)

    elif ultra.distance() < 150:
        robot.straight(160)
    else:
        robot.turn(-90)
        robot.straight(400)
        Move_One_Block_Forward_Right_Plus()
        Move_One_Block_Forward_Right_Plus()
        Move_One_Block_Forward_Right_Plus()
        Move_One_Block_Forward_Right_Plus()

def Turning_For_Seeking_Object_in_Black_Zone():# 90도 회전하여 1,2 옆의 라인에 있는 물체 찾기
    robot.straight(40)
    robot.turn(100)
    if ultra.distance() < 400:
        Far_Seeking()
        Grab_Object()
        
    elif ultra.distance() < 800:
        Move_One_Block_Forward_Left_Minus()
        Far_Seeking()
        Grab_Object()

    else:
        robot.turn(-90)
        pass

def Turning_For_Seeking_Object_in_Black_Zone2():# 90도 회전하여 3 옆의 라인에 있는 물체 찾기
    robot.straight(40)
    robot.turn(100)
    if ultra.distance() < 800:
        Move_One_Block_Forward_Right_Plus()
        Grab_Object()
    else:
        robot.turn(-90)

def Far_Seeking(): # 가까이서 물체를 인식한다
    while left_cs.color() != Color.BLACK :
        rate= gain * -(right_cs.reflection() - th)
        robot.drive(250,rate)

        if ultra.distance() < 70:
            robot.stop()
            break

def Straight_Seeking(): #1, 2, 3번에서 물건 찾기
    if ultra.distance() < 400:
        Far_Seeking()
        Grab_Object()
    else:
        Move_One_Block_Forward_Right_Plus()

def Turning_90(): # 후진하면서 회전하기
    while robot.straight(-25):
        robot.turn(-90)
        robot.stop()

# # 여기서부터 시작
Count = 0

grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)
ev3.speaker.beep()

Start()
Move_One_Block_Forward_Right_Plus()
Straight_Seeking() # 1번에 물체가 있는지 확인
if ID == 1:
    Go_to_Red()
    Red_End()
    Count += 1
elif ID == 2:
    Go_to_Blue1()
    Blue_End()
else:
    pass
    Move_One_Block_Forward_Right_Plus()
print('Count')
robot.straight(40)
robot.turn(100) 
if ultra.distance() < 400: # 5번에 물체가 있는지 확인
    Far_Seeking()
    Grab_Object()
    if ID == 1:
        robot.turn(90)
        robot.straight(250)
        while left_cs.color() != Color.RED:
            rate = gain * -(right_cs.reflection()-th)
            robot.drive(250,rate)
        robot.straight(70)

        grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)

        Red_End()
        Count += 1


    elif ID == 2: # 5번 파란색은 좀 다른 경우로
        robot.turn(90)
        robot.straight(250)
        robot.turn(-90)
        
        while right_cs.color() != Color.BLACK:
            rate = gain * (left_cs.reflection()-th)
            robot.drive(250, rate)
        robot.straight(47)
        robot.turn(100)

        while left_cs.color() != Color.BLUE:
            rate = gain * -(right_cs.reflection()-th)
            robot.drive(250,rate)
        robot.straight(70)
        grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)
        
        Blue_End()
    else:
        pass
    
elif ultra.distance() < 800: # 9번에 물체가 있는지 확인
    Move_One_Block_Forward_Left_Minus()
    Far_Seeking()
    Grab_Object()
    if ID == 1:
        robot.turn(90)
        robot.straight(250)
        robot.turn(90)
        Move_One_Block_Forward_Left_Minus()
        robot.turn(-90)

        while left_cs.color() != Color.RED:
            rate = gain * -(right_cs.reflection()-th)
            robot.drive(250,rate)
        robot.straight(70)
        
        grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)

        Red_End()
        
    elif ID == 2:
        robot.turn(90)
        robot.straight(250)

        while left_cs.color() != Color.BLUE:
            rate = gain * -(right_cs.reflection()-th)
            robot.drive(250,rate)
        robot.straight(70)
        
        grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)
        Blue_End()
else:
    robot.turn(-90)
    pass




# 여기는 메모 라인
"""
캔은 빨간색, 패트병은 파란색

White_Area() 함수 확인해보기(특히 이 함수는 좀 손 많이 볼 필요 있음)
-> 이쪽은 인터넷 찾아보면서 확인해보기

함수내에 함수 넣어보면서 오류 찾아보기
함수들 조합해서 원하는 결과 만들어보기

Gain 값, Threshold값에 따른 Move_One_Block 조절 

5번, 9번 구간에서 바로 파란색, 빨간색 구간으로 갈 수 있게 설정하기

Go_to_Blue, Go_to_Red 필요한가?

# 여기서 부터는 번호(159 2610 3711 4812)순서로 가는것
1번 라인만 확인해보기

# 여기는 1번
Move_One_Block_Forward_Right_Plus()
Grab_Object()
robot.turn(200)
Go_to_Red()
Red_End()


# 여기는 5번

Move_One_Block_Forward_Right_Plus()
Turning_For_Seeking_Object_in_Black_Zone()
robot.turn(200)
Move_One_Block_Forward_Right_Plus()
robot.turn(-90)
robot.straight(40)
Go_to_Red()
Red_End()



Move_One_Block_Forward_Right_Plus()
Turning_For_Seeking_Object_in_Black_Zone()
Go_to_Blue2()
Blue_End()


# 여기는 9번

Move_One_Block_Forward_Right_Plus()

Turning_For_Seeking_Object_in_Black_Zone()

robot.turn(200)
Move_One_Block_Forward_Right_Plus()
Move_One_Block_Forward_Right_Plus()

robot.turn(-90)
robot.straight(40)
Go_to_Red()
Red_End()


# 여기는 2번

Move_One_Block_Forward_Right_Plus()
Grab_Object()
robot.turn(200)
Move_One_Block_Forward_Left_Minus()
robot.straight(20)

Go_to_Red()
Red_End()

# 여기는 6번

Move_One_Block_Forward_Right_Plus()
Move_One_Block_Forward_Right_Plus()

Turning_For_Seeking_Object_in_Black_Zone()

robot.turn(200)
Move_One_Block_Forward_Left_Minus()
robot.turn(-90)
robot.straight(40)
Move_One_Block_Forward_Left_Minus()

Go_to_Red()
Red_End()

# 여기는 10번
Move_One_Block_Forward_Right_Plus()
Move_One_Block_Forward_Right_Plus()
Turning_For_Seeking_Object_in_Black_Zone()
robot.turn(200)
Move_One_Block_Forward_Left_Minus()
Move_One_Block_Forward_Left_Minus()
robot.turn(-90)
robot.straight(40)
Move_One_Block_Forward_Left_Minus()

Go_to_Red()
Red_End()


# 여기는 3번
Move_One_Block_Forward_Right_Plus()
Move_One_Block_Forward_Right_Plus()
Grab_Object()
robot.turn(200)
Move_One_Block_Forward_Left_Minus()
Move_One_Block_Forward_Left_Minus()
Go_to_Red()
Red_End()


# 여기는 7번
Move_One_Block_Forward_Right_Plus()
Move_One_Block_Forward_Right_Plus()
Move_One_Block_Forward_Right_Plus()
Turning_For_Seeking_Object_in_Black_Zone()
robot.turn(200)
Move_One_Block_Forward_Left_Minus()
robot.turn(-90)
robot.straight(40)
Move_One_Block_Forward_Left_Minus()
Move_One_Block_Forward_Left_Minus()

Go_to_Red()
Red_End()


# 여기는 11번

Move_One_Block_Forward_Right_Plus()
Move_One_Block_Forward_Right_Plus()
Move_One_Block_Forward_Right_Plus()

Turning_For_Seeking_Object_in_Black_Zone2()

robot.turn(200)
Move_One_Block_Forward_Left_Minus()
Move_One_Block_Forward_Left_Minus()
robot.turn(-90)
robot.straight(40)
Move_One_Block_Forward_Left_Minus()
Move_One_Block_Forward_Left_Minus()

Go_to_Red()
Red_End()

# 여기는 4번 구간


Move_One_Block_Forward_Right_Plus()
Move_One_Block_Forward_Right_Plus()
Move_One_Block_Forward_Right_Plus()

Grab_Object()

robot.straight(-288)
robot.turn(180)
Move_One_Block_Forward_Left_Minus()
Move_One_Block_Forward_Left_Minus()


#######################
# 여기 구간은 조합 구간


"""