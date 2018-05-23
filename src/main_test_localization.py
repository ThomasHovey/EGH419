import cv2
import numpy as np
#from picamera.array import PiRGBArray
#from picamera import PiCamera 
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

state.LeftMotorSpeed = 60
state.RightMotorSpeed = 50
# Init serial to arduino
comm.Serial_init()

# Create path list
pathx = []
pathy = []

# Setup plot
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(state.Pose.x, state.Pose.y, 'ro') # Returns a tuple of line objects, thus the comma
line2, = ax.plot(state.Pose.x, state.Pose.y, 'b.') # Returns a tuple of line objects, thus the comma
# Set limit
plt.ylim(-500,500)
plt.xlim(-500,500)

i=0
# Update motor speeds
comm.setMotorSpeed(state)
old_time = time.time()

while i < 15:
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

state.LeftMotorSpeed = 0
state.RightMotorSpeed = 0
comm.setMotorSpeed(state)

while(1):
	time.sleep(1)