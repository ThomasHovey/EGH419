import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera 
import time
import modules.place_recog as place_recog
from modules.classes.Pose import Pose
from modules.classes.ImageData import ImageData
from modules.classes.State import State
import modules.comm as comm
import modules.localization as localization
import matplotlib.pyplot as plt

time.sleep(0.1)

state = State()

comm.Serial_init()

# Setup plot
pathx = []
pathy = []
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(state.Pose.x, state.Pose.y, 'ro') # Returns a tuple of line objects, thus the comma
line2, = ax.plot(state.Pose.x, state.Pose.y, 'b.') # Returns a tuple of line objects, thus the comma
# Set limit
plt.ylim(-500,500)
plt.xlim(-500,500)
# Move foward and build database
state.LeftMotorSpeed = 50
state.RightMotorSpeed = 50


place_recog.database_append(state)

comm.setMotorSpeed(state)
old_time = time.time()
i=0
while i < 5:
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.Time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)
	# add points to path 
	pathx.append(state.Pose.x)
	pathy.append(state.Pose.y)
	# plot new position
	line1.set_xdata(state.Pose.x)
	line1.set_ydata(state.Pose.y)
	line2.set_xdata(pathx)
	line2.set_ydata(pathy)
	
	fig.canvas.draw()
	fig.canvas.flush_events()
	i += 1
	# Append new database point
	place_recog.database_append(state)

# Stop motor
state.LeftMotorSpeed = 0
state.RightMotorSpeed = 0
comm.setMotorSpeed(state)

# Finalize databse
database = place_recog.database_finalize()


# Move backwards until intial position reached
state.LeftMotorSpeed = -50
state.RightMotorSpeed = -50

# Update motor speeds
comm.setMotorSpeed(state)

i=0
while i < 50:

	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.Time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)
	# add points to path 
	pathx.append(state.Pose.x)
	pathy.append(state.Pose.y)
	# plot new position
	line1.set_xdata(state.Pose.x)
	line1.set_ydata(state.Pose.y)
	line2.set_xdata(pathx)
	line2.set_ydata(pathy)
	
	fig.canvas.draw()
	fig.canvas.flush_events()
	i += 1
	# Check position for start
	new_pose, error = place_recog.find_location(database, state.Pose)
	
	if new_pose.x == 0 and new_pose.y == 0:
		print("Back at start - shutting down")
		break

# Stop motor
state.LeftMotorSpeed = 0
state.RightMotorSpeed = 0
comm.setMotorSpeed(state)

