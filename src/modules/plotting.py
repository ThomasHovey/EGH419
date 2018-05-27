import numpy as np
import time
from classes.State import State
from classes.Pose import Pose
import matplotlib.pyplot as plt
import math

# Setup length of line for bearing
unit = 10

# Create path list
pathx = []
pathy = []
pathx_enc = []
pathy_enc = []
pathx_IMU = []
pathy_IMU = []
pathx_des = []
pathy_des = []
pathx_img = []
pathy_img = []

pose = Pose(0,0,0,0,0,0)

#Set limits
yneg = -100
ypos = 400
xneg = -100
xpos = 400
# Setup plot
plt.ion()
fig = plt.figure()
a = fig.add_subplot(111)
# Set limit
plt.ylim(yneg,ypos)
plt.xlim(xneg,xpos)
# b = fig.add_subplot(222)
# # Set limit
# plt.ylim(yneg,ypos)
# plt.xlim(xneg,xpos)
# c = fig.add_subplot(223)
# # Set limit
# plt.ylim(yneg,ypos)
# plt.xlim(xneg,xpos)
# d = fig.add_subplot(224)
# # Set limit
# plt.ylim(yneg,ypos)
# plt.xlim(xneg,xpos)

line1, = a.plot(pose.x, pose.y, 'r+') # Returns a tuple of line objects, thus the comma
line2, = a.plot(pose.x, pose.y, 'b.') # Returns a tuple of line objects, thus the comma
# Plot heading
heading1, = a.plot([pose.x, pose.x+unit*math.cos(pose.theta *(math.pi/180))], \
	[pose.y, pose.y+unit*math.sin(pose.theta *(math.pi/180))])

# line3, = b.plot(pose.x, pose.y, 'g.') # Returns a tuple of line objects, thus the comma
# line4, = c.plot(pose.x, pose.y, 'r.') # Returns a tuple of line objects, thus the comma
# line5, = d.plot(pose.x, pose.y, 'y.') # Returns a tuple of line objects, thus the comma




def update_plot(pose):
	# Update paths
	pathx.append(pose.x)
	pathy.append(pose.y)
	# pathx_des.append(desired.x)
	# pathy_des.append(desired.y)
	# pathx_enc.append(encoder.x)
	# pathy_enc.append(encoder.y)
	# pathx_IMU.append(IMU.x)
	# pathy_IMU.append(IMU.y)

def updata_plot_img(pose):
	pathx.append(pose.x)
	pathy.append(pose.y)
		


def draw_plot(pose):
	
	# Update data
	line1.set_xdata(pose.x)
	line1.set_ydata(pose.y)
	line2.set_xdata(pathx)
	line2.set_ydata(pathy)
	heading1.set_xdata([pose.x, pose.x+unit*math.cos(pose.theta *(math.pi/180))])
	heading1.set_ydata([pose.y, pose.y+unit*math.sin(pose.theta *(math.pi/180))])

	# Draw
	fig.canvas.draw()
	fig.canvas.flush_events()






# line3.set_xdata(pathx_enc)
	# line3.set_ydata(pathy_enc)
	# line4.set_xdata(pathx_IMU)
	# line4.set_ydata(pathy_IMU)
	# line5.set_xdata(pathx_des)
	# line5.set_ydata(pathy_des)


	
	# heading3, = b.plot([encoder.x, encoder.x+unit*math.cos(encoder.theta *(math.pi/180))], \
	# 	[encoder.y, encoder.y+unit*math.sin(encoder.theta *(math.pi/180))])
	# heading4, = c.plot([IMU.x, IMU.x+unit*math.cos(IMU.theta *(math.pi/180))], \
	# 	[IMU.y, IMU.y+unit*math.sin(IMU.theta *(math.pi/180))])
	# heading5, = d.plot([desired.x, desired.x+unit*math.cos(desired.theta *(math.pi/180))], \
	# 	[desired.y, desired.y+unit*math.sin(desired.theta *(math.pi/180))])
