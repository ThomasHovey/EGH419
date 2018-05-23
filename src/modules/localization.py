import numpy as np
from classes.State import State
from classes.Pose import Pose
import math


WIDTH = 100.0
Vdr = 3
Vdl = 3 
trust_value_imu = 0.0
trust_value_encoder = 1.0
trust_value_desired =  0.0

def map_encoder(state):

	# Get l and r velocities
	Vr = state.RightDistance/state.Time
	Vl = state.LeftDistance/state.Time

	# Get angular velocity
	omega = (Vr - Vl)/WIDTH

	# Get Velocity
	V = (Vr+Vl)/2

	# Create new pose value for veolcity
	pose = Pose(0,0,0,0,0,0)

	# Calculate new positions
	pose.omega = omega
	pose.x_vel = V*math.cos(state.Pose.theta +omega*state.Time)
	pose.y_vel = V*math.sin(state.Pose.theta +omega*state.Time)

	return pose

def map_IMU_data(state):
	# Calculate new pose from imu data
	x_accel = state.IMU.x_accel
	y_accel = state.IMU.y_accel
	z_gyro = state.IMU.z_gyro 

	# Create a new pose value for velocity
	pose = Pose(0,0,0,0,0,0)

	#Intergrate these 3 values ^ over time  to find these values  
	pose.omega = state.Pose.omega + z_gyro * state.Time # intergrate z_gyro over time
	pose.x_vel =  state.Pose.x_vel + x_accel * state.Time # intergrate x_accel to get x_vel
	pose.y_vel =  state.Pose.y_vel + y_accel * state.Time #intergrate y_accel to get y_vel

	return pose

def get_desired_vel(state):
	Vdr =state.RightMotorSpeed
	Vdl =state.LeftMotorSpeed
	
	# Angular Velocity
	omega = (Vdr - Vdl)/WIDTH
	
	# Get Velocity
	V = (Vdr+Vdl)/2
	
	# Create new pose value for veolcity
	pose = Pose(0,0,0,0,0,0)

	# Calculate new positions
	pose.omega = omega
	# The old heading Plus the new change in angular velocity times by time to achieve new heading  
	pose.x_vel = V*math.cos(state.Pose.theta + omega*state.Time)
	pose.y_vel = V*math.sin(state.Pose.theta + omega*state.Time)
	
	return pose
	
	
	
# localization state
def update(state):


	encoder_vel = map_encoder(state)
	IMU_vel = map_IMU_data(state)
	desired_vel = get_desired_vel(state)
	
	
	pose = Pose(0,0,0,0,0,0)
	
	# Perform weighting and divided by 3 to get an average
	pose.omega = ((encoder_vel.omega * trust_value_encoder) + (IMU_vel.omega * trust_value_imu) + (desired_vel.omega * trust_value_desired))
	
	pose.x_vel = ((encoder_vel.x_vel * trust_value_encoder) + (IMU_vel.x_vel * trust_value_imu) + (desired_vel.x_vel * trust_value_desired))
	
	pose.y_vel = ((encoder_vel.y_vel * trust_value_encoder) + (IMU_vel.y_vel * trust_value_imu) + (desired_vel.y_vel * trust_value_desired))
	


	# Get position according to the encoders
	# Old position plus the new change in position to achieve new position
	pose.theta = state.Pose.theta + pose.omega * state.Time
	pose.x = state.Pose.x + pose.x_vel * state.Time
	pose.y = state.Pose.y + pose.y_vel * state.Time
	

	state.Pose = pose
	
	
	return


	
	
	
	
	
