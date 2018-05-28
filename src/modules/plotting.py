import numpy as np
import time
from classes.State import State
from classes.Pose import Pose
import matplotlib.pyplot as plt
import math

# Setup length of line for bearing
unit = 15

# Create path list
pathx = []
pathy = []
pathx_boundary = []
pathy_boundary = []

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

line_boundary, = a.plot(pose.x, pose.y, 'r+') # Returns a tuple of line objects, thus the comma
line_path, = a.plot(pose.x, pose.y, 'b.') # Returns a tuple of line objects, thus the comma
# Plot heading
heading, = a.plot([pose.x, pose.x+unit*math.cos(pose.theta *(math.pi/180))], \
	[pose.y, pose.y+unit*math.sin(pose.theta *(math.pi/180))])

def add_database(database):
	for i in database:
		pathx_boundary.append(database[i].pose.x)
		pathy_boundary.append(database[i].pose.y)

def update_plot(pose):
	# Update paths
	pathx.append(pose.x)
	pathy.append(pose.y)

def updata_plot_img(pose):
	pathx.append(pose.x)
	pathy.append(pose.y)
		


def draw_plot(pose):
	
	# Update data
	line_boundary.set_xdata(pathx_boundary)
	line_boundary.set_ydata(pathy_boundary)
	line_path.set_xdata(pathx)
	line_path.set_ydata(pathy)
	heading.set_xdata([pose.x, pose.x+unit*math.cos(pose.theta *(math.pi/180))])
	heading.set_ydata([pose.y, pose.y+unit*math.sin(pose.theta *(math.pi/180))])

	# Draw
	fig.canvas.draw()
	fig.canvas.flush_events()




########################
# dead code
########################

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
