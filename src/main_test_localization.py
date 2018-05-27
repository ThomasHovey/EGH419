#import cv2
import numpy as np
#from picamera.array import PiRGBArray
#from picamera import PiCamera 
import time
import modules.place_recog as place_recog
from modules.classes.Pose import Pose
from modules.classes.ImageData import ImageData
from modules.classes.State import State
import modules.plotting as plotting
import modules.comm as comm
import modules.localization as localization
import matplotlib.pyplot as plt
import math

time.sleep(0.1)

# Init state
state = State()

# Init serial to arduino
comm.Serial_init()
plotting.init_plot()

# Set motor speeds
state.LeftMotorSpeed = 0
state.RightMotorSpeed = 0
comm.setMotorSpeed(state)

# Loop
old_time = time.time()
i = 0
while i < 100:
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.Time = time.time() - old_time
	old_time = time.time()
	# Update localization
	encoder,IMU,desired = localization.update(state)

	# Update plot
	plotting.update_plot(state.Pose, encoder, IMU, desired)

	i += 1

# Stop
state.LeftMotorSpeed = 0
state.RightMotorSpeed = 0
comm.setMotorSpeed(state)

# Draw Plot
plotting.draw_plot(state.Pose, encoder, IMU, desired)

print("X")
print(state.Pose.x)
print("Y")
print(state.Pose.y)
print("Theta")
print(state.Pose.theta)


while(1):
	time.sleep(1)