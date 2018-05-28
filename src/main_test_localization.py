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
import modules.nav as nav
import matplotlib.pyplot as plt
import math

time.sleep(0.1)

# Init state
state = State()

# Init serial to arduino
comm.Serial_init()



##################
# Move to (300,0)
##################

desired_pos = Pose(300,0,0,0,0,0)
# Loop
old_time = time.time()
while state.pose.x < 300 :
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)

	# Update plot
	plotting.update_plot(state.pose)
	
	# Get motor speeds and update
	nav.moveToPoint(state, desired_pos)
	comm.setMotorSpeed(state)


# Stop
state.leftMotorSpeed = 0
state.rightMotorSpeed = 0
comm.setMotorSpeed(state)

# Draw Plot
plotting.draw_plot(state.pose)


##################
# Move to (300,300)
##################

desired_pos = Pose(300,300,0,0,0,0)
# Loop
old_time = time.time()
while state.pose.y < 300 :
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)

	# Update plot
	plotting.update_plot(state.pose)
	
	# Get motor speeds and update
	nav.moveToPoint(state, desired_pos)
	comm.setMotorSpeed(state)


# Stop
state.leftMotorSpeed = 0
state.rightMotorSpeed = 0
comm.setMotorSpeed(state)

# Draw Plot
plotting.draw_plot(state.pose)

##################
# Move to (0,300)
##################

desired_pos = Pose(0,300,0,0,0,0)
# Loop
old_time = time.time()
while state.pose.x > 0 :
	# Read encoder data ect
	comm.updateData(state)	
	# Find time 
	state.time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)

	# Update plot
	plotting.update_plot(state.pose)
	
	# Get motor speeds and update
	nav.moveToPoint(state, desired_pos)
	comm.setMotorSpeed(state)


# Stop
state.leftMotorSpeed = 0
state.rightMotorSpeed = 0
comm.setMotorSpeed(state)

# Draw Plot
plotting.draw_plot(state.pose)

##################
# Move to (0,0)
##################

desired_pos = Pose(0,0,0,0,0,0)
# Loop
old_time = time.time()
while state.pose.y > 0 :
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)

	# Update plot
	plotting.update_plot(state.pose)
	
	# Get motor speeds and update
	nav.moveToPoint(state, desired_pos)
	comm.setMotorSpeed(state)

# Stop
state.leftMotorSpeed = 0
state.rightMotorSpeed = 0
comm.setMotorSpeed(state)

# Draw Plot
plotting.draw_plot(state.pose)

##################
# Move to (300,300)
##################

desired_pos = Pose(300,300,0,0,0,0)
# Loop
old_time = time.time()
while state.pose.x < 300 :
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)

	# Update plot
	plotting.update_plot(state.pose)
	
	# Get motor speeds and update
	nav.moveToPoint(state, desired_pos)
	comm.setMotorSpeed(state)

# Stop
state.leftMotorSpeed = 0
state.rightMotorSpeed = 0
comm.setMotorSpeed(state)

# Draw Plot
plotting.draw_plot(state.pose)

print('X')
print(state.pose.x)

print('Y')
print(state.pose.y)
print('Theta')
print(state.pose.theta)


while(1):
	time.sleep(1)