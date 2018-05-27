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
while state.Pose.x < 300 :
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.Time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)

	# Update plot
	plotting.update_plot(state.Pose)
	
	# Get motor speeds and update
	nav.moveToPoint(state, desired_pos)
	comm.setMotorSpeed(state)


# Stop
state.LeftMotorSpeed = 0
state.RightMotorSpeed = 0
comm.setMotorSpeed(state)

# Draw Plot
plotting.draw_plot(state.Pose)


##################
# Move to (300,300)
##################

desired_pos = Pose(300,300,0,0,0,0)
# Loop
old_time = time.time()
while state.Pose.y < 300 :
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.Time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)

	# Update plot
	plotting.update_plot(state.Pose)
	
	# Get motor speeds and update
	nav.moveToPoint(state, desired_pos)
	comm.setMotorSpeed(state)


# Stop
state.LeftMotorSpeed = 0
state.RightMotorSpeed = 0
comm.setMotorSpeed(state)

# Draw Plot
plotting.draw_plot(state.Pose)

##################
# Move to (0,300)
##################

desired_pos = Pose(0,300,0,0,0,0)
# Loop
old_time = time.time()
while state.Pose.x > 0 :
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.Time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)

	# Update plot
	plotting.update_plot(state.Pose)
	
	# Get motor speeds and update
	nav.moveToPoint(state, desired_pos)
	comm.setMotorSpeed(state)


# Stop
state.LeftMotorSpeed = 0
state.RightMotorSpeed = 0
comm.setMotorSpeed(state)

# Draw Plot
plotting.draw_plot(state.Pose)

##################
# Move to (0,0)
##################

desired_pos = Pose(0,0,0,0,0,0)
# Loop
old_time = time.time()
while state.Pose.y > 0 :
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.Time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)

	# Update plot
	plotting.update_plot(state.Pose)
	
	# Get motor speeds and update
	nav.moveToPoint(state, desired_pos)
	comm.setMotorSpeed(state)

# Stop
state.LeftMotorSpeed = 0
state.RightMotorSpeed = 0
comm.setMotorSpeed(state)

# Draw Plot
plotting.draw_plot(state.Pose)

##################
# Move to (300,300)
##################

desired_pos = Pose(300,300,0,0,0,0)
# Loop
old_time = time.time()
while state.Pose.x < 300 :
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.Time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)

	# Update plot
	plotting.update_plot(state.Pose)
	
	# Get motor speeds and update
	nav.moveToPoint(state, desired_pos)
	comm.setMotorSpeed(state)

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