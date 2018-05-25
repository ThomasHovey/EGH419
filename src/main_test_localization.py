#import cv2
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

state.LeftMotorSpeed = 50
state.RightMotorSpeed = 50
# Init serial to arduino
comm.Serial_init()

# Create path list
pathx = []
pathy = []
pathx_enc = []
pathy_enc = []
pathx_IMU = []
pathy_IMU = []
pathx_des = []
pathy_des = []
# Setup plot
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(state.Pose.x, state.Pose.y, 'r+') # Returns a tuple of line objects, thus the comma
line2, = ax.plot(state.Pose.x, state.Pose.y, 'b.') # Returns a tuple of line objects, thus the comma
line3, = ax.plot(state.Pose.x, state.Pose.y, 'g.') # Returns a tuple of line objects, thus the comma
line4, = ax.plot(state.Pose.x, state.Pose.y, 'r.') # Returns a tuple of line objects, thus the comma
line5, = ax.plot(state.Pose.x, state.Pose.y, 'y.') # Returns a tuple of line objects, thus the comma

# Set limit
plt.ylim(-500,500)
plt.xlim(-500,500)

i=0
# Update motor speeds
# comm.setMotorSpeed(state)
old_time = time.time()
# ##
# while state.Pose.x < 200:
# 	# Read encoder data ect
# 	comm.updateData(state)
# 	# Find time 
# 	state.Time = time.time() - old_time
# 	old_time = time.time()
# 	# Update localization
# 	localization.update(state)
# 	# add points to path 
# 	pathx.append(state.Pose.x)
# 	pathy.append(state.Pose.y)
# 	# plot new position
# 	#line1.set_xdata(state.Pose.x)
# 	#line1.set_ydata(state.Pose.y)
# 	#line2.set_xdata(pathx)
# 	#line2.set_ydata(pathy)
	
# 	#fig.canvas.draw()
# 	#fig.canvas.flush_events()
# 	i += 1


# while state.Pose.x < 200:
# 	# Read encoder data ect
# 	comm.updateData(state)
# 	# Find time 
# 	state.Time = time.time() - old_time
# 	old_time = time.time()
# 	# Update localization
# 	encoder,IMU,desired = localization.update(state)
# 	# add points to path 
# 	pathx.append(state.Pose.x)
# 	pathy.append(state.Pose.y)
# 	pathx_des.append(desired.x)
# 	pathy_des.append(desired.y)
# 	pathx_enc.append(encoder.x)
# 	pathy_enc.append(encoder.y)
# 	pathx_IMU.append(IMU.x)
# 	pathy_IMU.append(IMU.y)
# 	# plot new position
# 	#line1.set_xdata(state.Pose.x)
# 	#line1.set_ydata(state.Pose.y)
# 	#line2.set_xdata(pathx)
# 	#line2.set_ydata(pathy)
	
# 	#fig.canvas.draw()
# 	#fig.canvas.flush_events()
# 	i += 1

# # Stop
# state.LeftMotorSpeed = 0
# state.RightMotorSpeed = 0
# comm.setMotorSpeed(state)

# # Update plot
# # line1.set_xdata(state.Pose.x)
# # line1.set_ydata(state.Pose.y)
# # line2.set_xdata(pathx)
# # line2.set_ydata(pathy)
# line3.set_xdata(pathx_enc)
# line3.set_ydata(pathy_enc)
# line4.set_xdata(pathx_IMU)
# line4.set_ydata(pathy_IMU)
# # line5.set_xdata(pathx_des)
# # line5.set_ydata(pathy_des)

# fig.canvas.draw()
# fig.canvas.flush_events()
# print("X - pos")
# print(state.Pose.x)

# Turn
state.LeftMotorSpeed = -25
state.RightMotorSpeed = 25
comm.setMotorSpeed(state)


# Update motor speeds
comm.setMotorSpeed(state)
old_time = time.time()

while state.Pose.theta < 90:
	print("Theta")
	print(state.Pose.theta)
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
	#line1.set_xdata(state.Pose.x)
	#line1.set_ydata(state.Pose.y)
	#line2.set_xdata(pathx)
	#line2.set_ydata(pathy)

# Stop
state.LeftMotorSpeed = 0
state.RightMotorSpeed = 0
comm.setMotorSpeed(state)

heading1, = ax.plot(state.Pose.x*math.cos(state.Pose.Theta *(math.pi/180)),state.Pose.y*math.sin(state.Pose.Theta *(math.pi/180)))
heading3, = ax.plot(encoder.x*math.cos(encoder.Theta *(math.pi/180)),encoder.y*math.sin(encoder.Theta *(math.pi/180)))
heading4, = ax.plot(IMU.x*math.cos(IMU.Theta *(math.pi/180)),IMU.y*math.sin(IMU.Theta *(math.pi/180)))
heading5, = ax.plot(desired.x*math.cos(desired.Theta *(math.pi/180)),desired.y*math.sin(desired.Theta *(math.pi/180)))
# Update plot
line1.set_xdata(state.Pose.x)
line1.set_ydata(state.Pose.y)
line2.set_xdata(pathx)
line2.set_ydata(pathy)

fig.canvas.draw()
fig.canvas.flush_events()

print("Theta")
print(state.Pose.theta)

# # Move foward
# state.LeftMotorSpeed = 30
# state.RightMotorSpeed = 30
# comm.setMotorSpeed(state)
# old_time = time.time()

# while state.Pose.y < 200:
# 	# Read encoder data ect
# 	comm.updateData(state)
# 	# Find time 
# 	state.Time = time.time() - old_time
# 	old_time = time.time()
# 	# Update localization
# 	localization.update(state)
# 	# add points to path 
# 	pathx.append(state.Pose.x)
# 	pathy.append(state.Pose.y)
	
# # Update plot
# line1.set_xdata(state.Pose.x)
# line1.set_ydata(state.Pose.y)
# line2.set_xdata(pathx)
# line2.set_ydata(pathy)

# fig.canvas.draw()
# fig.canvas.flush_events()

# # Stop
# state.LeftMotorSpeed = 0
# state.RightMotorSpeed = 0
# comm.setMotorSpeed(state)

while(1):
	time.sleep(1)