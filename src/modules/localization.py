import numpy as np
from classes.State import State
from classes.Pose import Pose
import math

WIDTH = 20.0

def map_encoder(state):

	# Get l and r velocities
	Vr = state.RightDistance/state.Time
	Vl = state.LeftDistance/state.Time

	# Get angular velocity
	omega = (Vr - Vl)/WIDTH

	# Get Velocity
	V = (Vr+Vl)/2

	# Create new pose value
	new_pose = Pose(0,0,0)

	# Calculate new positions
	new_pose.theta = omega*state.Time + state.Pose.theta
	new_pose.x = V*math.cos(new_pose.theta)*state.Time + state.Pose.x
	new_pose.y = V*math.sin(new_pose.theta)*state.Time + state.Pose.y

	# Update State
	state.Pose = new_pose

