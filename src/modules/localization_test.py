import numpy as np
import time
from classes.State import State
from classes.Pose import Pose
import localization
import matplotlib.pyplot as plt

state = State()

# Add distance
state.LeftDistance = 0.2
state.RightDistance = 0.5
state.Time = 0.01

# Setup plot
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(state.Pose.x, state.Pose.y, 'ro') # Returns a tuple of line objects, thus the comma
plt.ylim(-50,50)
plt.xlim(-50,50)

# Do 100 time steps
i=0
while i < 100:
	localization.update(state)	
	
	# plot new position
	line1.set_xdata(state.Pose.x)
	line1.set_ydata(state.Pose.y)
	fig.canvas.draw()
	fig.canvas.flush_events()
	i += 1
	time.sleep(0.1)



