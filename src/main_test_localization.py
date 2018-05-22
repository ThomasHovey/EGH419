import cv2
import numpy as np
#from picamera.array import PiRGBArray
#from picamera import PiCamera 
import time
import modules.place_recog as place_recog
from modules.classes.Pose import Pose
from modules.classes.ImageData import ImageData
import modules.comm as comm
import modules.localization as localization

time.sleep(0.1)

state.LeftMotorSpeed = 50
state.RightMotorSpeed = 70
comm.Serial_init()
# Setup plot
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(state.Pose.x, state.Pose.y, 'ro') # Returns a tuple of line objects, thus the comma
plt.ylim(-50,50)
plt.xlim(-50,50)

i=0
while i < 10:
	# Update motor speeds
	comm.setMotorSpeed(state)

	time.sleep(0.2)
	# Read encoder data ect
	comm.updateData(state)
	localization.update(state)
	# plot new position
	line1.set_xdata(state.Pose.x)
	line1.set_ydata(state.Pose.y)
	fig.canvas.draw()
	fig.canvas.flush_events()
	i += 1

state.LeftMotorSpeed = 0
state.RightMotorSpeed = 0
comm.sendMotorSpeeds(state)

