import numpy as np
import time
from classes.State import State
from classes.Pose import Pose
import comm
import matplotlib.pyplot as plt

READ_ENCODERS = "<ECD:>"


# Setup serial 
comm.Serial_init()

# Create a new 
state = State()

# Update motorspeed
state.LeftMotorSpeed = 140
state.RightMotorSpeed = -140
comm.SerialSendCommand(state,READ_ENCODERS)