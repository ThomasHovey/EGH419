#import cv2
import numpy as np
#from picamera.array import PiRGBArray
#from picamera import PiCamera 
import time
#import place_recog as place_recog
from classes.Pose import Pose
from classes.ImageData import ImageData
from classes.State import State
import plotting as plotting
import comm as comm
import localization as localization
import matplotlib.pyplot as plt
import math

time.sleep(0.1)

# Init state
state = State()

# Init serial to arduino
comm.Serial_init()

# Set motor speeds
state.leftMotorSpeed = 0
state.rightMotorSpeed = 0
comm.setMotorSpeed(state)

# Loop
old_time = time.time()
i = 0
while 1:
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)

	# Update plot
	plotting.update_plot(state.pose)
	if i == 5:
		plotting.draw_plot(state.pose)
		i = 0


	i += 1

# Stop
state.leftMotorSpeed = 0
state.rightMotorSpeed = 0
comm.setMotorSpeed(state)

# Draw Plot
plotting.draw_plot(state.pose)

