import numpy as np
import time
from classes.State import State
from classes.Pose import Pose
import comm

State.LeftMotorSpeed = 140
State.RightMotorSpeed = -140

READ_ENCODERS = "<ECD:>"
READ_IMU = "<IMU:>"
READ_COMPASS = "<MAG:>"
READ_ALL = "<ALL:>"
SENT_SPEED = "<MoSp:" + str(State.LeftMotorSpeed) + "," + str(State.RightMotorSpeed) + ">"

# Setup serial 
comm.Serial_init()
print("Complete initialise Serial.")

# Create a new 
state = State()
time.sleep(2)

# Update encoders
comm.SerialSendCommand(state,"<ECD:>")
time.sleep(5)

# Update IMU
comm.SerialSendCommand(state,READ_IMU)
time.sleep(5)

# Update Compass
comm.SerialSendCommand(state,READ_COMPASS)
time.sleep(5)

# Update all encoders, IMU, Compass
comm.SerialSendCommand(state,READ_ALL)
time.sleep(5)

# Update motorspeed
comm.SerialSendCommand(state,SENT_SPEED)
time.sleep(5)
