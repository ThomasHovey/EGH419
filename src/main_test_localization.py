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

# Set motor speeds
state.LeftMotorSpeed = 30
state.RightMotorSpeed = 30
comm.setMotorSpeed(state)

# Loop
old_time = time.time()
i = 0
while state.Pose.x < 200 :
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.Time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)

	# Update plot
	plotting.update_plot(state.Pose)
	if i == 5:
		plotting.draw_plot(state.Pose)
		i = 0

	i += 1

# Stop
state.LeftMotorSpeed = 0
state.RightMotorSpeed = 0
comm.setMotorSpeed(state)

# Draw Plot
plotting.draw_plot(state.Pose)


# Set motor speeds
state.LeftMotorSpeed = -13
state.RightMotorSpeed = 13
comm.setMotorSpeed(state)

# Loop
old_time = time.time()
i = 0
while state.Pose.theta < 90 or state.Pose.theta > 200 :
	print(state.Pose.theta)
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.Time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)

	# Update plot
	plotting.update_plot(state.Pose)
	if i == 5:
		plotting.draw_plot(state.Pose)
		i = 0

	i += 1

# Stop
state.LeftMotorSpeed = 0
state.RightMotorSpeed = 0
comm.setMotorSpeed(state)

# Draw Plot
plotting.draw_plot(state.Pose)

# Set motor speeds
state.LeftMotorSpeed = 25
state.RightMotorSpeed = 25
comm.setMotorSpeed(state)

# Loop
old_time = time.time()
i = 0
while state.Pose.y < 200 :
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.Time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)

	# Update plot
	plotting.update_plot(state.Pose)
	if i == 5:
		plotting.draw_plot(state.Pose)
		i = 0

	i += 1

# Stop
state.LeftMotorSpeed = 0
state.RightMotorSpeed = 0
comm.setMotorSpeed(state)

# Draw Plot
plotting.draw_plot(state.Pose)


print('X')
print(state.Pose.x)

print('Y')
print(state.Pose.y)
print('Theta')
print(state.Pose.theta)


while(1):
	time.sleep(1)