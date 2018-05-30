import threading, time, sys
import numpy as np
import time
from classes.State import State
from classes.Pose import Pose
from classes.ImageData import ImageData
import matplotlib.pyplot as plt
import math

# Setup length of line for bearing
unit = 40

# Create path list
pathx = []
pathy = []
pathx_boundary = []
pathy_boundary = []
pathx_img = []
pathy_img = []
pathx_img_robot = []
pathy_img_robot = []


last_pose = Pose(0,0,0,0,0,0)

#Set limits
yneg = -200
ypos = 1000
xneg = -200
xpos = 1000
# Setup plot
plt.ion()
fig = plt.figure()
a = fig.add_subplot(111)
# Set limit
plt.ylim(yneg,ypos)
plt.xlim(xneg,xpos)

line_boundary, = a.plot(last_pose.x, last_pose.y, 'r.') # Returns a tuple of line objects, thus the comma
line_path, = a.plot(last_pose.x, last_pose.y, 'b.') # Returns a tuple of line objects, thus the comma
line_img, = a.plot(last_pose.x, last_pose.y, 'g*') # Returns a tuple of line objects, thus the comma
line_img_robot, = a.plot(last_pose.x, last_pose.y, 'go')
# Plot heading
heading, = a.plot([last_pose.x, last_pose.x+unit*math.cos(last_pose.theta *(math.pi/180))], \
	[last_pose.y, last_pose.y+unit*math.sin(last_pose.theta *(math.pi/180))])

# Threading
lock_drawing = threading.Lock()


def add_database(database):
	while True:
		acquired = lock_drawing.acquire(0)
		if acquired:
			break
	global pathx_boundary
	global pathy_boundary

	pathx_boundary = []
	pathy_boundary = []
	for i in database:
		pathx_boundary.append(i.pose.x)
		pathy_boundary.append(i.pose.y)
	lock_drawing.release()


def update_plot(pose):
	global last_pose
	while True:
		acquired = lock_drawing.acquire(0)
		if acquired:
			break
	# Update paths
	pathx.append(pose.x)
	pathy.append(pose.y)
	last_pose = pose
	lock_drawing.release()

def update_plot_img(robot, pose):
	while True:
		acquired = lock_drawing.acquire(0)
		if acquired:
			break
	pathx_img.append(pose.x)
	pathy_img.append(pose.y)
	pathx_img_robot.append(robot.x)
	pathy_img_robot.append(robot.y)
	lock_drawing.release()
		


def draw_plot():
	
	# Update data
	line_boundary.set_xdata(pathx_boundary)
	line_boundary.set_ydata(pathy_boundary)
	line_path.set_xdata(pathx)
	line_path.set_ydata(pathy)
	line_img.set_xdata(pathx_img)
	line_img.set_ydata(pathy_img)
	line_img_robot.set_xdata(pathx_img_robot)
	line_img_robot.set_ydata(pathy_img_robot)
	heading.set_xdata([last_pose.x, last_pose.x+unit*math.cos(last_pose.theta *(math.pi/180))])
	heading.set_ydata([last_pose.y, last_pose.y+unit*math.sin(last_pose.theta *(math.pi/180))])

	# Draw
	fig.canvas.draw()
	fig.canvas.flush_events()


def plotting_main():
	while True:
		acquired = lock_drawing.acquire(0)
		if acquired:
			break
	
	line_boundary.set_xdata(pathx_boundary)
	line_boundary.set_ydata(pathy_boundary)
	line_path.set_xdata(pathx)
	line_path.set_ydata(pathy)

	heading.set_xdata([last_pose.x, last_pose.x+unit*math.cos(last_pose.theta *(math.pi/180))])
	heading.set_ydata([last_pose.y, last_pose.y+unit*math.sin(last_pose.theta *(math.pi/180))])

	# Draw
	fig.canvas.draw()
	fig.canvas.flush_events()
	lock_drawing.release()
	time.sleep(0.01)

