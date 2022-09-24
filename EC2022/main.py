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
white = 62
th = (black + white) / 2
gain = 0.8

grab_motor = Motor(Port.A)

# Write your program here.

# 여기는 함수를 적는 라인
def Start():
    grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)
    robot.straight(160)

def Go_Home():
    while left_cs.color() != Color.GREEN:
            rate = gain * -(right_cs.reflection() - th)
            robot.drive(230, rate)
    robot.turn(-98)
    robot.straight(100)
    
#물체를 인식하여 집어드는 함수
def Grab_Object():
    while True:
        blocks = h1.get_blocks()
        if len(blocks) > 0:
            global ID
            ID = blocks[0].ID
            wait(500)
            if ID == 1:
                robot.straight(70)
                robot.stop()
                grab_motor.run_until_stalled(200,then = Stop.COAST,duty_limit = 50)
                break
            elif ID == 2:
                robot.straight(70)
                robot.stop()
                grab_motor.run_until_stalled(200,then = Stop.COAST,duty_limit = 50)
                break
            else:
                pass
            wait(500)


def Go_to_Red():  #원점(1번)에서 빨간색으로 출발
    Move_One_Block_Forward_Left_Minus()
    robot.turn(-96)
    Move_One_Block_Forward_Right_Plus()
    robot.turn(98)

    Release_On_Red()

def Go_to_Blue():
    Move_One_Block_Forward_Left_Minus()
    robot.turn(-96)

    Move_One_Block_Forward_Right_Plus()
    Move_One_Block_Forward_Right_Plus()
    robot.turn(98)

    Release_On_Blue()

def Release_On_Red():
    while left_cs.color() != Color.RED:
        rate = gain * -(right_cs.reflection()-th)
        robot.drive(230,rate)
    robot.straight(70)

    grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)

def Release_On_Blue():
    while right_cs.color() != Color.BLUE:
        rate = gain * (left_cs.reflection()-th)
        robot.drive(230,rate)
    
    robot.straight(70)
    grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)

def Red_End(): # 빨간색에 놓고 뒤로 돌아 90도 회전 이후 1번으로 간다
    robot.straight(-90)
    robot.turn(190)
    Move_One_Block_Forward_Right_Plus()
    robot.turn(-96)
    Move_One_Block_Forward_Left_Minus()
    robot.turn(98)
    Move_One_Block_Forward_Right_Plus()
        
def Blue_End(): # 파란색에 놓고 뒤로 돌아 90도 회전 이후 1번으로 간다
    robot.straight(-90)
    robot.turn(190)
    Move_One_Block_Forward_Left_Minus()
    robot.turn(-80)
    Move_One_Block_Forward_Left_Minus()
    Move_One_Block_Forward_Left_Minus()
    robot.turn(98)
    Move_One_Block_Forward_Right_Plus()

def Far_Seeking_Right(): # 3번에서는 안됨
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(200,rate)
        if ultra.distance() < 80:
            robot.stop()
            break

def Far_Seeking_Left(): # 3번에서는 안됨
    while left_cs.color() != Color.BLACK :
        rate= gain * -(right_cs.reflection() - th)
        robot.drive(200,rate)
        if ultra.distance() < 80:
            robot.stop()
            break

def Move_One_Block_Forward_Right_Plus():
    while right_cs.color() != Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(230,rate)
    while right_cs.color() == Color.BLACK :
        rate= gain * (left_cs.reflection() - th)
        robot.drive(230,rate)
    robot.stop()

def Move_One_Block_Forward_Left_Minus():
    while left_cs.color() != Color.BLACK :
        rate= gain * -(right_cs.reflection() - th)
        robot.drive(230,rate)

    while left_cs.color() == Color.BLACK :
        rate= gain * -(right_cs.reflection() - th)
        robot.drive(230,rate)
    robot.stop()


############################################################################ 여기서부터 시작

# 이곳은 1층 라인(1,5,9번)
Start()
Move_One_Block_Forward_Right_Plus()
robot.straight(150)
if ultra.distance() < 60:
    Grab_Object() # 1번에 물체가 있는지 확인
    if ID == 1:
        robot.turn(180)
        Go_to_Red()
        Red_End()

    elif ID == 2:
        robot.turn(180)
        Go_to_Blue()
        Blue_End()
        
else:
    Move_One_Block_Forward_Right_Plus()    
    
robot.turn(98)


if ultra.distance() < 400: # 5번에 물체가 있는지 확인
    
    Far_Seeking_Right()
    Grab_Object()
    if ID == 1:
        robot.straight(70)
        robot.turn(98)
        robot.straight(270)
    
        Release_On_Red()
        Red_End()

        robot.turn(98) # 여기는 5번을 끝내고 9번을 하는 경우

        if ultra.distance() < 810:
            Far_Seeking_Right()
            Grab_Object()

            if ID == 1: # 9번에 캔인 경우
                robot.straight(70)
                robot.turn(98)
                robot.straight(270)
                robot.turn(98)
                Move_One_Block_Forward_Left_Minus()
                robot.turn(-96)

                Release_On_Red()
                Red_End()
                
            elif ID == 2:
                robot.straight(70)
                robot.turn(98)
                robot.straight(270)
                Release_On_Blue()
                Blue_End()            
        else:
            robot.turn(-96)

    elif ID == 2: # 5번 플라스틱인 경우(9번 거친거 아님)
        robot.straight(70)
        robot.turn(98)
        robot.straight(270)
        robot.turn(-90)
        robot.straight(40)

        Move_One_Block_Forward_Right_Plus()
        robot.turn(98)

        Release_On_Blue()        
        Blue_End()
        
        # 5번에서 플라스틱을 찾고 9번에 물체 확인
        robot.turn(98)
        if ultra.distance() < 810:

            Far_Seeking_Right()
            Grab_Object()

            if ID == 1: #9번에 캔이 있는 경우
                robot.straight(70)
                robot.turn(98)
                robot.straight(270)
                robot.turn(98)
                Move_One_Block_Forward_Left_Minus()
                robot.turn(-96)

                Release_On_Red()
                Red_End()
        
            elif ID == 2: # 9번에 플라스틱이 있는 경우
                robot.straight(70)
                robot.turn(98)
                robot.straight(270)

                Release_On_Blue()
                Blue_End()
        else:
            robot.turn(-96)

elif ultra.distance() < 810: # 5번에 물체가 없고 9번에 물체가 있는 경우
    
    Far_Seeking_Right()
    Grab_Object()
    
    if ID == 1:
        robot.straight(70)
        robot.turn(98)
        robot.straight(270)
        robot.turn(96)
    
        Move_One_Block_Forward_Left_Minus()
        robot.turn(-96)

        Release_On_Red()
        Red_End()
        
    elif ID == 2: # 9번 파란색은 좀 다른 경우로
        robot.straight(70)
        robot.turn(98)
        robot.straight(270)

        Release_On_Blue()
        Blue_End()
        
else:
    robot.turn(-96)

##############################################################################
# 여기는 2번라인(2,6,10)
robot.straight(300)

if ultra.distance() < 58:

    Grab_Object() # 2번에 물체가 있는지 확인
    if ID == 1:
        robot.turn(180)
        Move_One_Block_Forward_Left_Minus()
        Go_to_Red()
        Red_End()
        Move_One_Block_Forward_Right_Plus()
        
    elif ID == 2:
        robot.turn(180)
        Move_One_Block_Forward_Left_Minus()
        Go_to_Blue()
        Blue_End()
        Move_One_Block_Forward_Right_Plus()        
else:
    Move_One_Block_Forward_Right_Plus()

robot.turn(99)

if ultra.distance() < 400: # 6번에 물체가 있는지 확인

    Far_Seeking_Right()
    Grab_Object()
    if ID == 1:
        robot.straight(70)
        robot.turn(98)
        Move_One_Block_Forward_Right_Plus()
        robot.straight(270)
    
        Release_On_Red()
        Red_End()
        Move_One_Block_Forward_Right_Plus()
        robot.turn(98) # 여기는 6번을 끝내고 10번을 하는 경우
        if ultra.distance() < 810:
            
            Move_One_Block_Forward_Right_Plus()
            Far_Seeking_Right()
            Grab_Object()
        
            if ID == 1: # 10번에 캔인 경우
        
                robot.straight(70)
                robot.turn(98)
                Move_One_Block_Forward_Right_Plus()
                robot.straight(270)
                robot.turn(98)
                Move_One_Block_Forward_Left_Minus()
                robot.turn(-96)

                Release_On_Red()
                Red_End()
                Move_One_Block_Forward_Right_Plus()
            
            elif ID == 2: #10번이 플라스틱인 경우
        
                robot.straight(70)
                robot.turn(98)
                Move_One_Block_Forward_Right_Plus()
                robot.straight(270)
                
                Release_On_Blue()
                Blue_End()
                Move_One_Block_Forward_Right_Plus()
        else:
            robot.turn(-96)

    elif ID == 2: # 6번 플라스틱인 경우(10번 거친거 아님)
        
        robot.straight(70)
        robot.turn(98)
        Move_One_Block_Forward_Left_Minus()
        robot.straight(270)
        robot.turn(-92)
        robot.straight(40)
        Move_One_Block_Forward_Right_Plus()
        robot.turn(97)

        Release_On_Blue()
        Blue_End()
        Move_One_Block_Forward_Right_Plus()
        # 6번에서 플라스틱을 찾고 10번에 물체 확인
        robot.turn(98)

        if ultra.distance() < 810:
            Move_One_Block_Forward_Right_Plus()
            Far_Seeking_Right()
            Grab_Object()

            if ID == 1: #10번에 캔이 있는 경우
                robot.straight(70)
                robot.turn(98)
                Move_One_Block_Forward_Right_Plus()
                
                robot.straight(270)

                robot.turn(98)
                Move_One_Block_Forward_Left_Minus()
                robot.turn(-96)

                Release_On_Red()
                Red_End()
                Move_One_Block_Forward_Right_Plus()
            
            elif ID == 2: # 10번에 플라스틱이 있는 경우
                robot.straight(70)
                robot.turn(98)
                Move_One_Block_Forward_Left_Minus()
                robot.straight(270)
                
                Release_On_Blue()
                Blue_End()
                Move_One_Block_Forward_Right_Plus()
        else:
            robot.turn(-96)    

elif ultra.distance() < 810: # 6번에 물체가 없고 10번에 물체가 있는 경우
    
    Move_One_Block_Forward_Right_Plus()
    Far_Seeking_Right()
    Grab_Object()
    if ID == 1: #10번에 캔이 있는 경우
        robot.straight(70)
        robot.turn(98)
        Move_One_Block_Forward_Right_Plus()
        robot.straight(270)
        robot.turn(96)
        Move_One_Block_Forward_Left_Minus()
        robot.turn(-96)

        Release_On_Red()
        Red_End()
        Move_One_Block_Forward_Right_Plus()
        
    elif ID == 2: # 10번 파란색은 좀 다른 경우로
        robot.straight(70)
        robot.turn(98)
        Move_One_Block_Forward_Right_Plus()
        robot.straight(270)

        Release_On_Blue()
        Blue_End()
        Move_One_Block_Forward_Right_Plus()
        
else:
    robot.turn(-96)


###############################################################################################
# 여기는 3번 라인(3,7,11)
robot.straight(300)

if ultra.distance() < 58:
    
    Grab_Object() # 1번에 물체가 있는지 확인
    if ID == 1:
        robot.turn(180)
        Move_One_Block_Forward_Left_Minus()
        Move_One_Block_Forward_Left_Minus()
        Go_to_Red()
        Red_End()
        Move_One_Block_Forward_Right_Plus()
        Move_One_Block_Forward_Right_Plus()
    elif ID == 2:
        robot.turn(180)
        Move_One_Block_Forward_Left_Minus()
        Move_One_Block_Forward_Left_Minus()
        Go_to_Blue()
        Blue_End()
        Move_One_Block_Forward_Right_Plus()
        Move_One_Block_Forward_Right_Plus()
else:
    Move_One_Block_Forward_Right_Plus()

robot.turn(98)

if ultra.distance() < 400: # 7번에 물체가 있는지 확인
    Far_Seeking_Right()
    Grab_Object()
    if ID == 1:
        robot.straight(70)
        robot.turn(98)
        Move_One_Block_Forward_Right_Plus()
        Move_One_Block_Forward_Right_Plus()
        robot.straight(270)
        
        Release_On_Red()
        Red_End()
        # 여기는 7번을 끝내고 11번을 하는 경우
        Move_One_Block_Forward_Right_Plus()
        Move_One_Block_Forward_Right_Plus()
        robot.turn(98)
        if ultra.distance() < 810:
            Move_One_Block_Forward_Right_Plus()
            Far_Seeking_Right()
            Grab_Object()
            if ID == 1: # 11번에 캔인 경우  
                
                robot.straight(70)
                robot.turn(98)
                Move_One_Block_Forward_Right_Plus()
                Move_One_Block_Forward_Right_Plus()
                robot.straight(270)
                robot.turn(98)
                Move_One_Block_Forward_Left_Minus()
                robot.turn(-96)

                Release_On_Red()
                Red_End()
                Move_One_Block_Forward_Right_Plus()
                Move_One_Block_Forward_Right_Plus()

            elif ID == 2: #11번이 플라스틱인 경우
                robot.straight(70)
                robot.turn(98)
                Move_One_Block_Forward_Right_Plus()
                Move_One_Block_Forward_Right_Plus()
                robot.straight(270)
                
                Release_On_Blue()
                Blue_End()
                Move_One_Block_Forward_Right_Plus()
                Move_One_Block_Forward_Right_Plus()
        else:
            robot.turn(-96)
    elif ID == 2: # 7번 플라스틱인 경우(11번 거친거 아님)
        robot.straight(70)
        robot.turn(98)
        Move_One_Block_Forward_Left_Minus()
        Move_One_Block_Forward_Left_Minus()
        robot.straight(270)
        robot.turn(-96)
        robot.straight(40)
        Move_One_Block_Forward_Right_Plus()
        robot.turn(98)

        Release_On_Blue()
        Blue_End()
        Move_One_Block_Forward_Right_Plus()
        Move_One_Block_Forward_Right_Plus()
        # 7번에서 플라스틱을 찾고 11번에 물체 확인
        robot.turn(98)
        if ultra.distance() < 810:
            
            Move_One_Block_Forward_Right_Plus() # 나중에는 if를 사용하여 물체 있는지 우선 확인
            Far_Seeking_Right()
            Grab_Object()

            if ID == 1: #11번에 캔이 있는 경우
            
                robot.straight(70)
                robot.turn(98)

                Move_One_Block_Forward_Right_Plus()
                Move_One_Block_Forward_Right_Plus()
                
                robot.straight(270)
                robot.turn(98)
                Move_One_Block_Forward_Left_Minus()
                robot.turn(-96)

                Release_On_Red()
                Red_End()
                Move_One_Block_Forward_Right_Plus()
                Move_One_Block_Forward_Right_Plus()
            
            elif ID == 2: # 11번에 플라스틱이 있는 경우
            
                robot.straight(70)
                robot.turn(98)
                Move_One_Block_Forward_Right_Plus()
                Move_One_Block_Forward_Right_Plus()
                robot.straight(270)

                Release_On_Blue()
                Blue_End()
                Move_One_Block_Forward_Right_Plus()
                Move_One_Block_Forward_Right_Plus()
        else:
            robot.turn(-96)

elif ultra.distance() < 810: # 7번에 물체가 없고 11번에 물체가 있는 경우
    
    Move_One_Block_Forward_Right_Plus()
    Far_Seeking_Right()
    Grab_Object()
    if ID == 1: #11번에 캔이 있는 경우
        robot.straight(70)
        robot.turn(98)
        Move_One_Block_Forward_Right_Plus()
        Move_One_Block_Forward_Right_Plus()
        robot.straight(270)
        robot.turn(96) 
        Move_One_Block_Forward_Left_Minus()
        robot.turn(-96)

        Release_On_Red()
        Red_End()
        Move_One_Block_Forward_Right_Plus()
        Move_One_Block_Forward_Right_Plus()

    elif ID == 2: # 11번 파란색은 좀 다른 경우로
        robot.straight(70)
        robot.turn(98)
        Move_One_Block_Forward_Right_Plus()
        Move_One_Block_Forward_Right_Plus()

        robot.straight(270)

        Release_On_Blue()
        Blue_End()
        Move_One_Block_Forward_Right_Plus()
        Move_One_Block_Forward_Right_Plus()
else:
    robot.turn(-98)
   
if ultra.distance() < 400:
    robot.straight(350)
    Grab_Object()
    robot.turn(180)
    robot.straight(400)
    for i in range(4):
        Move_One_Block_Forward_Left_Minus()
    
    if ID == 1:
        Go_to_Red()
        
        Go_Home()
    elif ID == 2:
        Go_to_Blue()

        Go_Home()
else:
    robot.turn(180)
    for i in range(6):
        Move_One_Block_Forward_Left_Minus()

    
robot.straight(100)



# 여기는 메모 라인

"""
함수내에 함수 넣어보면서 오류 찾아보기
함수들 조합해서 원하는 결과 만들어보기
빛에 따른 reflection값 때문에 th 값이 변한다. 그럴때 Gain값을 어떻게 조절할지에 대해 확인
각도는 96도
Grab_Object()
if ID == 2:
    robot.straight(250)
    while right_cs.color() != Color.BLACK:
        rate = 3 * gain * (left_cs.reflection() - th)
        robot.drive(-200, rate)
    while right_cs.color() == Color.BLACK:
        rate = 3 * gain * (left_cs.reflection() - th)
        robot.drive(-200, rate)
    
    Move_One_Block_Forward_Left_Minus()
    robot.straight(270)
    
robot.straight(70)
grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)

위 코드는 5번에서 물체를 잡고 앞으로 전진 후 뒤로 -90도 회전을 하며 후진을 한다
"""