#import cv2
import numpy as np
#from picamera.array import PiRGBArray
#from picamera import PiCamera 
import time
import place_recog as place_recog
from classes.Pose import Pose
from classes.ImageData import ImageData
from classes.State import State
import plotting as plotting
import comm as comm
import localization as localization
import nav as nav
import matplotlib.pyplot as plt
import math

time.sleep(0.1)

# Init state
state = State()

# Init serial to arduino
comm.Serial_init()


##################
# Move to (500,500)
##################

desired_pos = Pose(500,500,0,0,0,0)
old_time = time.time()
	
while abs(state.pose.x - desired_pos.x) > 10 or abs(state.pose.y - desired_pos.y) > 10  :
	# print("Desired x:" + str(desired_pos.x) + " y:" + str(desired_pos.y))
	# print("Current x:" + str(state.pose.x) + " x:" +str(state.pose.y) + " theta:" + str(state.pose.theta))


	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)
	plotting.update_plot(state.pose)


	# Get motor speeds and update
	nav.moveToPoint(state, desired_pos)
	comm.setMotorSpeed(state)
	# Add img to database
	database = place_recog.database_append(state.pose)


print("Reached Node Point")
# Stop
state.leftMotorSpeed = 0
state.rightMotorSpeed = 0
comm.setMotorSpeed(state)


# Plot database locations

# Draw Plot
plotting.draw_plot()


while(1):
	time.sleep(1)