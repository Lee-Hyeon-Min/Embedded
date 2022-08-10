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

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Calculate the light threshold. Choose values based on your measurements.
BLACK = 9
WHITE = 85
threshold = (BLACK + WHITE) / 2

# Set the drive speed at 100 millimeters per second.
DRIVE_SPEED = 100

# Set the gain of the proportional line controller. This means that for every
# percentage point of light deviating from the threshold, we set the turn
# rate of the drivebase to 1.2 degrees per second.

# For example, if the light value deviates from the threshold by 10, the robot
# steers at 10*1.2 = 12 degrees per second.
PROPORTIONAL_GAIN = 1.2

# Start following the line endlessly.
while True:
    deviation = line_sensor.reflection() - threshold # 문턱으로부터 변화율을 계산한다
    turn_rate = PROPORTIONAL_GAIN * deviation # 돌림율 계산
    robot.drive(DRIVE_SPEED, turn_rate) # 기본운전속도와 돌림비율 설정
    wait(10) # You can wait for a short time or do other things in this loop.


grab_motor.run_until_stalled(-200, then = Stop.COAST, duty_limit=50) #집게를 펼치는 신호, 200이면 집게를 접는 것이다

