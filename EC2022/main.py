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

black_left = 8
black_right = 10
white_left = 72
white_right = 71
th_left = (black_left + white_left) / 2
th_right = (black_right + white_right) / 2
gain = 0.8
grab_motor = Motor(Port.A)
Object_Count = 0
# Write your program here.

# 여기는 함수를 적는 라인
def Start():
    grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)
    robot.straight(160)

#물체를 인식하여 집어드는 함수
def Grab_Object():
    while True:
        blocks = h1.get_blocks()
        if len(blocks) > 0:
            global ID
            global Count
            Count = 0
            ID = blocks[0].ID
            wait(500)
            if ID == 1:
                robot.straight(25)
                robot.stop()
                grab_motor.run_until_stalled(200,then = Stop.COAST,duty_limit = 50)
                Count += 1
                break
            elif ID == 2:
                robot.straight(20)
                robot.stop()
                grab_motor.run_until_stalled(200,then = Stop.COAST,duty_limit = 50)
                Count += 1
                break
            else:
                pass
            wait(500)


def Go_to_Red():  #원점(1번)에서 빨간색으로 출발
    while left_cs.color() != Color.BLACK:
        rate = gain * -(right_cs.reflection()-th_right)
        robot.drive(250,rate)
    robot.straight(60)
    robot.turn(-100)
    
    while right_cs.color() != Color.BLACK:
        rate = gain * (left_cs.reflection()-th_left)
        robot.drive(250, rate)
    robot.straight(60)

    robot.turn(100)

    while left_cs.color() != Color.RED:
        rate = gain * -(right_cs.reflection()-th_right)
        robot.drive(250,rate)

    robot.straight(100)
    grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)

def Go_to_Blue():
    while left_cs.color() != Color.BLACK:
        rate = gain * -(right_cs.reflection()-th_right)
        robot.drive(250,rate)
    robot.straight(60)
    robot.turn(-100)

    while right_cs.color() != Color.BLACK:
        rate = gain * (left_cs.reflection()-th_left)
        robot.drive(250, rate)
    
    while right_cs.color() == Color.BLACK:
        rate = gain * (left_cs.reflection()-th_left)
        robot.drive(250, rate)
    
    while right_cs.color() != Color.BLACK:
        rate = gain * (left_cs.reflection()-th_left)
        robot.drive(250, rate)
    robot.straight(47)
    robot.turn(100)

    while right_cs.color() != Color.BLUE:
        rate = gain * (left_cs.reflection()-th_left)
        robot.drive(250,rate)
    robot.straight(100)
    grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)

def Release_On_Red():
    while left_cs.color() != Color.RED:
        rate = gain * -(right_cs.reflection()-th_right)
        robot.drive(240,rate)
    robot.straight(100)
    grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)
    
def Release_On_Blue():
    while right_cs.color() != Color.BLUE:
        rate = gain * (left_cs.reflection()-th_left)
        robot.drive(250,rate)

    robot.straight(100)
    grab_motor.run_until_stalled(-200,then = Stop.COAST,duty_limit = 50)    
    
def Red_End(): # 빨간색에 놓고 뒤로 돌아 90도 회전 이후 1번으로 간다
    robot.straight(-100)
    robot.turn(182)
    Move_One_Block_Forward_Left_Minus()
    robot.turn(-95)
    Move_One_Block_Forward_Left_Minus()
    robot.turn(100)
    Move_One_Block_Forward_Right_Plus()
    
def Blue_End(): # 파란색에 놓고 뒤로 돌아 90도 회전 이후 1번으로 간다
    robot.straight(-100)
    robot.turn(190)
    Move_One_Block_Forward_Left_Minus()
    robot.turn(-100)
    Move_Two_Block_Forward_Left_Minus()
    robot.turn(100)
    Move_One_Block_Forward_Right_Plus()

def Far_Seeking_Right(): # 3번에서는 안됨
    while right_cs.color() != Color.BLACK:
        rate= gain * (left_cs.reflection() - th_left)
        robot.drive(250,rate)
        if ultra.distance() < 80:
            robot.stop()
            break
        else:
            pass
    while right_cs.color() == Color.BLACK:
        rate = gain * (left_cs.reflection() - th_left)
        robot.drive(250,rate)
    robot.stop()
            

def Move_One_Block_Forward_Right_Plus():
    while right_cs.color() != Color.BLACK:
        rate= gain * (left_cs.reflection() - th_left)
        robot.drive(250,rate)

    while right_cs.color() == Color.BLACK :
        rate= gain * (left_cs.reflection() - th_left)
        robot.drive(250,rate)
    robot.stop()
                
def Move_One_Block_Forward_Left_Minus():
    while left_cs.color() != Color.BLACK:
        rate= gain * -(right_cs.reflection() - th_right)
        robot.drive(250,rate)

    while left_cs.color() == Color.BLACK:
        rate= gain * -(right_cs.reflection() - th_right)
        robot.drive(250,rate)
    robot.stop()



def Move_Two_Block_Forward_Right_Plus():
    for i in range(2):
        Move_One_Block_Forward_Right_Plus()

def Move_Two_Block_Forward_Left_Minus():
    for i in range(2):
        Move_One_Block_Forward_Left_Minus()

############################################################################ 여기서부터 시작
# 이곳은 1층 라인(1,5,9번)
Start()
while Object_Count != 6:
    Move_One_Block_Forward_Right_Plus()
    Far_Seeking_Right()

    if ultra.distance() < 80:
        Grab_Object() # 1번에 물체가 있는지 확인

        if ID == 1:
            robot.turn(190)
            Go_to_Red()
            Red_End()
            Object_Count += Count
            
        elif ID == 2:
            robot.turn(190)
            Go_to_Blue()
            Blue_End()
            Object_Count += Count
            
    else:
        pass

    robot.turn(108)

    if ultra.distance() < 400: # 5번에 물체가 있는지 확인
        
        Far_Seeking_Right()
        Grab_Object()
        
        if ID == 1:
            robot.straight(90)
            robot.turn(100)
            robot.straight(270)
            Release_On_Red()
            Red_End()
            Object_Count += Count
            # 여기는 5번을 끝내고 9번을 하는 경우
            
            robot.turn(108)
            if ultra.distance() < 770:
                Far_Seeking_Right()
                Grab_Object()
            
                if ID == 1: # 9번에 캔인 경우
                    robot.straight(60)
                    robot.turn(100)
                    robot.straight(270)
                    robot.turn(100)
                    Move_One_Block_Forward_Left_Minus()
                    robot.turn(-100)
                    Release_On_Red()
                    Red_End()
                    Object_Count += Count
                elif ID == 2:
                    robot.straight(60)
                    robot.turn(100)
                    robot.straight(270)
                    Release_On_Blue()
                    Blue_End()    
                    Object_Count += Count        
            else:
                robot.turn(-100)

        elif ID == 2: # 5번 플라스틱인 경우(9번 거친거 아님)
            robot.straight(90)
            robot.turn(100)
            robot.straight(270)
            robot.turn(-100)
            
            Move_One_Block_Forward_Right_Plus()

            robot.turn(100)

            Release_On_Blue()
            Blue_End()
            Object_Count += Count
            # 5번에서 플라스틱을 찾고 9번에 물체 확인
            
            robot.turn(100)
            if ultra.distance() < 770:
                Far_Seeking_Right()
                Grab_Object()
                
                if ID == 1: #9번에 캔이 있는 경우
                    robot.straight(60)
                    robot.turn(100)
                    robot.straight(270)
                    robot.turn(100)
                    
                    Move_One_Block_Forward_Left_Minus()
                    robot.turn(-100)

                    Release_On_Red()
                    Red_End()
                    Object_Count += Count
                elif ID == 2: # 9번에 플라스틱이 있는 경우
                    robot.straight(60)
                    robot.turn(96)
                    robot.straight(270)
                    Release_On_Blue()
                    Blue_End()
                    Object_Count += Count
                    
            else:
                robot.turn(-100)

    elif ultra.distance() < 770: # 5번에 물체가 없고 9번에 물체가 있는 경우
        Far_Seeking_Right()
        Grab_Object()
        if ID == 1:
            robot.straight(60)
            robot.turn(100)
            robot.straight(270)
            robot.turn(100)
            Move_One_Block_Forward_Left_Minus()
            robot.turn(-100)

            Release_On_Red()
            Red_End()
            Object_Count += Count
        elif ID == 2: # 9번 파란색은 좀 다른 경우로
            robot.straight(60)
            robot.turn(96)
            robot.straight(270)

            Release_On_Blue()
            Blue_End()
            Object_Count += Count
    else:
        robot.turn(-100)

    ##############################################################################
    # 여기는 2번라인(2,6,10)
    Far_Seeking_Right()

    if ultra.distance() < 80:
        Grab_Object() # 1번에 물체가 있는지 확인

        if ID == 1:
            robot.turn(190)
            Move_One_Block_Forward_Left_Minus()
            Go_to_Red()
            Red_End()
            Object_Count += Count
            Move_One_Block_Forward_Right_Plus()
        elif ID == 2:
            robot.turn(190)
            Move_One_Block_Forward_Left_Minus()
            Go_to_Blue()
            Blue_End()
            Object_Count += Count
            Move_One_Block_Forward_Right_Plus()
    else:
        pass

    robot.turn(108)

    if ultra.distance() < 400: # 6번에 물체가 있는지 확인

        Far_Seeking_Right()
        Grab_Object()
        
        if ID == 1:
            robot.straight(90)
            robot.turn(100)
            Move_One_Block_Forward_Left_Minus()
            robot.straight(270)
        
            Release_On_Red()
            Red_End()
            Object_Count += Count
            Move_One_Block_Forward_Right_Plus()
        
            robot.turn(108) # 여기는 6번을 끝내고 10번을 하는 경우
            if ultra.distance() < 770:
                
                Move_One_Block_Forward_Right_Plus()
                Far_Seeking_Right()
                Grab_Object()
                if ID == 1: # 10번에 캔인 경우
                    robot.straight(60)
                    robot.turn(100)
                    Move_One_Block_Forward_Right_Plus()
                    robot.straight(270)
                    robot.turn(100)
                    Move_One_Block_Forward_Left_Minus()
                    robot.turn(-100)

                    Release_On_Red()
                    Red_End()
                    Object_Count += Count
                    Move_One_Block_Forward_Right_Plus()
                    
                elif ID == 2: #10번이 플라스틱인 경우
                    robot.straight(60)
                    robot.turn(100)
                    Move_One_Block_Forward_Right_Plus()
                    robot.straight(270)
                    
                    Release_On_Blue()
                    Blue_End()
                    Object_Count += Count
                    Move_One_Block_Forward_Right_Plus()
                    
            else:
                robot.turn(-100)

        elif ID == 2: # 6번 플라스틱인 경우(10번 거친거 아님)
            robot.straight(90)
            robot.turn(100)
            Move_One_Block_Forward_Left_Minus()
            robot.straight(280)
            robot.turn(-100)
            
            Move_One_Block_Forward_Right_Plus()
            robot.turn(100)

            Release_On_Blue()
            Blue_End()
            Object_Count += Count
            Move_One_Block_Forward_Right_Plus()
            
            # 6번에서 플라스틱을 찾고 10번에 물체 확인
            robot.turn(100)
            if ultra.distance() < 770:
                Move_One_Block_Forward_Right_Plus()
                Far_Seeking_Right()
                Grab_Object()
                if ID == 1: #10번에 캔이 있는 경우
                    robot.straight(60)
                    robot.turn(100)
                    Move_One_Block_Forward_Right_Plus()
                    
                    robot.straight(270)

                    robot.turn(100)
                    Move_One_Block_Forward_Left_Minus()
                    robot.turn(-100)
                    Release_On_Red()
                    Red_End()
                    Object_Count += Count
                    Move_One_Block_Forward_Right_Plus()
                
                elif ID == 2: # 10번에 플라스틱이 있는 경우
                    robot.straight(60)
                    robot.turn(100)
                    Move_One_Block_Forward_Left_Minus()
                    robot.straight(270)
                    Release_On_Blue()
                    Blue_End()
                    Object_Count += Count
                    Move_One_Block_Forward_Right_Plus()
            else:
                robot.turn(-100)    

    elif ultra.distance() < 770: # 6번에 물체가 없고 10번에 물체가 있는 경우
        
        Move_One_Block_Forward_Right_Plus()
        Far_Seeking_Right()
        Grab_Object()

        if ID == 1: #10번에 캔이 있는 경우
            robot.straight(60)
            robot.turn(100)
            Move_One_Block_Forward_Right_Plus()
            robot.straight(270)
            robot.turn(100)
            Move_One_Block_Forward_Left_Minus()
            robot.turn(-100)

            Release_On_Red()
            Red_End()
            Object_Count += Count
            Move_One_Block_Forward_Right_Plus()
            
        elif ID == 2: # 10번 파란색은 좀 다른 경우로
            robot.turn(-100)
            robot.turn(100)
            Move_One_Block_Forward_Right_Plus()
            robot.straight(270)

            Release_On_Blue()
            Blue_End()
            Object_Count += Count
            Move_One_Block_Forward_Right_Plus()
            
    else:
        robot.turn(-100)

    ###############################################################################################
    # 여기는 3번 라인(3,7,11)
    Far_Seeking_Right()

    if ultra.distance() < 80:
        Grab_Object() # 1번에 물체가 있는지 확인

        if ID == 1:
            robot.turn(190)
            Move_Two_Block_Forward_Left_Minus()
            Go_to_Red()
            Red_End()
            Object_Count += Count
            Move_Two_Block_Forward_Right_Plus()
        elif ID == 2:
            robot.turn(190)
            Move_Two_Block_Forward_Left_Minus()
            Go_to_Blue()
            Blue_End()
            Object_Count += Count
            Move_Two_Block_Forward_Right_Plus()
    else:
        pass
    robot.turn(108)

    if ultra.distance() < 400: # 7번에 물체가 있는지 확인
        Far_Seeking_Right()
        Grab_Object()

        if ID == 1:
            robot.straight(90)
            robot.turn(100)
            Move_Two_Block_Forward_Left_Minus()
            robot.straight(270)
            Release_On_Red()
            Red_End()
            Object_Count += Count
            # 여기는 7번을 끝내고 11번을 하는 경우
            Move_Two_Block_Forward_Right_Plus()
            
            robot.turn(108)
            if ultra.distance() < 770:
                Move_One_Block_Forward_Right_Plus()
                Far_Seeking_Right()
                Grab_Object()

                if ID == 1: # 11번에 캔인 경우  
                    robot.straight(60)
                    robot.turn(100)
                    Move_Two_Block_Forward_Right_Plus()
                    robot.straight(270)
                    robot.turn(100)
                    robot.straight(30)
                    Move_One_Block_Forward_Left_Minus()
                    robot.turn(-100)

                    Release_On_Red()
                    Object_Count += Count
                    if Object_Count == 6:
                        break
                    Red_End()
                    Move_Two_Block_Forward_Right_Plus()
                    
                elif ID == 2: #11번이 플라스틱인 경우
                    robot.straight(60)
                    robot.turn(100)
                    Move_Two_Block_Forward_Right_Plus()
                    robot.straight(270)
                    
                    Release_On_Blue()
                    Blue_End()
                    Object_Count += Count
                    Move_Two_Block_Forward_Right_Plus()
                    
            else:
                robot.turn(-100)
        elif ID == 2: # 7번 플라스틱인 경우(11번 거친거 아님)
            robot.straight(90)
            robot.turn(100)
            Move_Two_Block_Forward_Left_Minus()
            robot.straight(280)
            robot.turn(-100)
            Move_One_Block_Forward_Right_Plus()
            
            robot.turn(100)
        
            Release_On_Blue()
            Object_Count += Count
            if Object_Count == 6:
                break
            Blue_End()
            Move_Two_Block_Forward_Right_Plus()
            # 7번에서 플라스틱을 찾고 11번에 물체 확인
            
            robot.turn(108)
            if ultra.distance() < 770:
                
                Move_One_Block_Forward_Right_Plus() # 나중에는 if를 사용하여 물체 있는지 우선 확인
                Far_Seeking_Right()
                Grab_Object()
                if ID == 1: #11번에 캔이 있는 경우
                    robot.straight(60)    
                    robot.turn(100)

                    Move_Two_Block_Forward_Right_Plus()
                    
                    robot.straight(270)
                    robot.turn(100)
                    Move_One_Block_Forward_Left_Minus()
                    robot.turn(-100)
                    Release_On_Red()
                    Object_Count += Count
                    if Object_Count == 6:
                        break
                    Red_End()
                    Move_Two_Block_Forward_Right_Plus()
                    
                elif ID == 2: # 11번에 플라스틱이 있는 경우
                    robot.straight(60)
                    robot.turn(100)
                    Move_Two_Block_Forward_Right_Plus()
                    robot.straight(270)

                    Release_On_Blue()
                    Object_Count += Count
                    if Object_Count == 6:
                        break
                    Blue_End()
                    Move_Two_Block_Forward_Right_Plus()
                    
            else:
                robot.turn(-100)

    elif ultra.distance() < 770: # 7번에 물체가 없고 11번에 물체가 있는 경우
        
        Move_One_Block_Forward_Right_Plus()
        Far_Seeking_Right()
        Grab_Object()
        if ID == 1: #11번에 캔이 있는 경우
            robot.straight(60)
            robot.turn(102)
            Move_Two_Block_Forward_Right_Plus()
            robot.straight(270)
            robot.turn(100)
            Move_One_Block_Forward_Left_Minus()
            robot.turn(-100)

            Release_On_Red()
            Object_Count += Count
            if Object_Count == 6:
                break
            Red_End()
            Move_Two_Block_Forward_Right_Plus()
            
        elif ID == 2: # 11번 파란색은 좀 다른 경우로
            robot.straight(60)
            robot.turn(100)
            Move_Two_Block_Forward_Right_Plus()
            robot.straight(270)

            Release_On_Blue()
            Object_Count += Count
            if Object_Count == 6:
                break
            Blue_End()
            Move_Two_Block_Forward_Right_Plus()
            
    else:
        robot.turn(-100)
        
    #####################################################################
    # 여기는 4번 라인
    
    
    if ultra.distance() < 350: # 2번에서 4번 물체가 있을 때
        
        robot.straight(310)
        Grab_Object()
        if ID == 1: # 4번 물체가 캔
            robot.straight(-350)
            robot.turn(190)
            Move_Two_Block_Forward_Left_Minus()
            Go_to_Red()
            Object_Count += Count
            if Object_Count == 6:
                break
            Red_End()
            Move_Two_Block_Forward_Right_Plus()
            robot.turn(100)
            Move_One_Block_Forward_Right_Plus()
            robot.turn(-100)
        elif ID == 2:
            robot.straight(-350)
            robot.turn(190)
            Move_Two_Block_Forward_Left_Minus()
            Go_to_Blue()
            Object_Count += Count
            if Object_Count == 6:
                break
            Blue_End()
            Move_Two_Block_Forward_Right_Plus()
            robot.turn(100)
            Move_One_Block_Forward_Right_Plus()
            robot.turn(-100)
    else:
        robot.turn(100)
        Move_One_Block_Forward_Right_Plus()
        robot.straight(30)
        robot.turn(-100)


    if ultra.distance() < 350:
        robot.straight(310)
        Grab_Object()
        if ID == 1:
            robot.straight(-350)
            robot.turn(190)
            Move_Two_Block_Forward_Left_Minus()
            robot.straight(270)
            Release_On_Red()
            Object_Count += Count
            if Object_Count == 6:
                break
            Red_End()
            Move_Two_Block_Forward_Right_Plus()
            robot.turn(100)
            Move_Two_Block_Forward_Right_Plus()
            robot.turn(-100)
        elif ID == 2:
            robot.straight(-350)
            robot.turn(100)
            Move_One_Block_Forward_Right_Plus()
            robot.turn(100)
            Move_Two_Block_Forward_Right_Plus()
            robot.straight(270)
            Release_On_Blue()
            Object_Count += Count
            if Object_Count == 6:
                break
            Blue_End()
            Move_Two_Block_Forward_Right_Plus()
            robot.turn(100)
            Move_Two_Block_Forward_Right_Plus()
            robot.turn(-100)
    else:
        robot.turn(100)
        Move_One_Block_Forward_Right_Plus()
        robot.straight(30)
        robot.turn(-106)


    if ultra.distance() < 350:
        robot.straight(310)
        Grab_Object()
        if ID == 1:
            robot.straight(-350)
            robot.turn(190)
            Move_Two_Block_Forward_Right_Plus()
            robot.straight(270)
            robot.turn(100)
            Move_One_Block_Forward_Left_Minus()
            robot.turn(-100)
            Release_On_Red()
            Object_Count += Count
            break
        elif ID == 2:
            robot.straight(-350)
            robot.turn(190)
            Move_Two_Block_Forward_Right_Plus()
            robot.straight(270)
            Release_On_Blue()
            Object_Count += Count
            break
    

robot.straight(-40)
robot.turn(100)
while left_cs.color() != Color.GREEN: # 끝날때 초록선까지 쭈욱 가기
    Move_One_Block_Forward_Left_Minus()
    if left_cs.color() == Color.GREEN:
        break

Move_One_Block_Forward_Right_Plus()

robot.turn(-90)
robot.straight(100)


