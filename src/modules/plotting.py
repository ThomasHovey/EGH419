import numpy as np
import time
from classes.State import State
from classes.Pose import Pose
import matplotlib.pyplot as plt


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


def init_plot(pose):
	# Setup plot
	plt.ion()
	fig = plt.figure()
	ax = fig.add_subplot(111)
	line1, = ax.plot(pose.x, pose.y, 'r+') # Returns a tuple of line objects, thus the comma
	line2, = ax.plot(pose.x, pose.y, 'b.') # Returns a tuple of line objects, thus the comma
	line3, = ax.plot(pose.x, pose.y, 'g.') # Returns a tuple of line objects, thus the comma
	line4, = ax.plot(pose.x, pose.y, 'r.') # Returns a tuple of line objects, thus the comma
	line5, = ax.plot(pose.x, pose.y, 'y.') # Returns a tuple of line objects, thus the comma

	# Set limit
	plt.ylim(-500,500)
	plt.xlim(-500,500)


def update_plot(pose, encoder, IMU, desired):
	# Update paths
	pathx.append(pose.x)
	pathy.append(pose.y)
	pathx_des.append(desired.x)
	pathy_des.append(desired.y)
	pathx_enc.append(encoder.x)
	pathy_enc.append(encoder.y)
	pathx_IMU.append(IMU.x)
	pathy_IMU.append(IMU.y)

def updata_plot_img(pose):
	pathx.append(pose.x)
	pathy.append(pose.y)
		


def draw_plot(pose, encoder, IMU, desired):
	
	# Update data
	line1.set_xdata(pose.x)
	line1.set_ydata(pose.y)
	line2.set_xdata(pathx)
	line2.set_ydata(pathy)
	line3.set_xdata(pathx_enc)
	line3.set_ydata(pathy_enc)
	line4.set_xdata(pathx_IMU)
	line4.set_ydata(pathy_IMU)
	line5.set_xdata(pathx_des)
	line5.set_ydata(pathy_des)

	# Plot heading
	heading1, = ax.plot([pose.x, pose.x+unit*math.cos(pose.theta *(math.pi/180))], \
		[pose.y, pose.y+unit*math.sin(pose.theta *(math.pi/180))])
	heading3, = ax.plot([encoder.x, encoder.x+unit*math.cos(encoder.theta *(math.pi/180))], \
		[encoder.y, encoder.y+unit*math.sin(encoder.theta *(math.pi/180))])
	heading4, = ax.plot([IMU.x, IMU.x+unit*math.cos(IMU.theta *(math.pi/180))], \
		[IMU.y, IMU.y+unit*math.sin(IMU.theta *(math.pi/180))])
	heading5, = ax.plot([desired.x, desired.x+unit*math.cos(desired.theta *(math.pi/180))], \
		[desired.y, desired.y+unit*math.sin(desired.theta *(math.pi/180))])

	# Draw
	fig.canvas.draw()
	fig.canvas.flush_events()

