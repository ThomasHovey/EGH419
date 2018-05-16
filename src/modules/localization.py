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
	vel = Pose(0,0,0)

	# Calculate new positions
	vel.theta = omega
	vel.x = V*math.cos(vel.theta)
	vel.y = V*math.sin(vel.theta)

	# Update State
	#state.Pose = vel
	return vel 

def map_IMU_data(state):
	# Calculate new pose from imu data
	state.IMU.x_accelorimiter

	#intergrate once for velocity acording to imu
	vel = Pose(0,0,0)

	return vel

def get_desired_vel(state):
	Vr =state.RightMotorSpeed

	return vel

def localize(state):
	encoder_vel = map_encoder(state)
	IMU_vel = map_IMU_data(state)
	desired_vel = get_desired_vel(state)
	
	# Combine all 3 


	# Multiply velocity by time and add previous pose 


	state.Pose = final_pose 
