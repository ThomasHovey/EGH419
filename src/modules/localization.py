import numpy as np
from classes.State import State
from classes.Pose import Pose
import math


WIDTH = 1.585
trust_value_imu = 0.0
trust_value_encoder = 1.0
trust_value_desired =  0.0
trust_value_imu_omega = 1.0
trust_value_encoder_omega = 0.0
trust_value_desired_omega =  0.0

a = 4.05

def map_encoder(state):

	# Get l and r velocities
	Vr = a*(state.rightDistance)/state.time
	Vl = a*(state.leftDistance)/state.time

	# Get angular velocity
	omega = (Vr - Vl)/WIDTH

	# Get Velocity
	V = (Vr+Vl)/2

	# Create new pose value for veolcity
	pose = Pose(0,0,0,0,0,0)

	# Calculate new positions
	pose.omega = omega
	pose.x_vel = V*math.cos((state.pose.theta +omega*state.time)*(math.pi/180))
	pose.y_vel = V*math.sin((state.pose.theta +omega*state.time)*(math.pi/180))

	return pose

def map_IMU_data(state):
	# Calculate new pose from imu data
	x_accel = state.IMU.y_accel *9806.65
	y_accel = state.IMU.x_accel * 9806.65
	z_gyro = -state.IMU.z_gyro 

	# Create a new pose value for velocity
	pose = Pose(0,0,0,0,0,0)

	# print("X_accel")
	# print(x_accel)
	#print("Y_accel")
	#print(y_accel)
	# print("Z_gyro")
	# print(z_gyro)

	#Intergrate these 3 values ^ over time  to find these values  
	pose.omega = z_gyro  # intergrate z_gyro over time
	pose.x_vel =  state.pose.x_vel + x_accel * state.time # intergrate x_accel to get x_vel
	pose.y_vel =  state.pose.y_vel + y_accel * state.time #intergrate y_accel to get y_vel

	return pose

def get_desired_vel(state):
	Vr =state.rightMotorSpeed*a
	Vl =state.leftMotorSpeed*a
	
	# Angular Velocity
	omega = (Vr - Vl)/WIDTH
	
	# Get Velocity
	V = (Vr+Vl)/2
	
	# Create new pose value for veolcity
	pose = Pose(0,0,0,0,0,0)

	# Calculate new positions
	pose.omega = omega
	# The old heading Plus the new change in angular velocity times by time to achieve new heading  
	pose.x_vel = V*math.cos((state.pose.theta +omega*state.time)*(math.pi/180))
	pose.y_vel = V*math.sin((state.pose.theta +omega*state.time)*(math.pi/180))
	
	return pose
	
	
	
# localization state
def update(state):


	encoder_vel = map_encoder(state)
	IMU_vel = map_IMU_data(state)
	desired_vel = get_desired_vel(state)
	
	
	pose = Pose(0,0,0,0,0,0)
	
	# Perform weighting and divided by 3 to get an average
	pose.omega = ((encoder_vel.omega * trust_value_encoder_omega) + (IMU_vel.omega * trust_value_imu_omega) + (desired_vel.omega * trust_value_desired_omega))
	
	pose.x_vel = ((encoder_vel.x_vel * trust_value_encoder) + (IMU_vel.x_vel * trust_value_imu) + (desired_vel.x_vel * trust_value_desired))
	
	pose.y_vel = ((encoder_vel.y_vel * trust_value_encoder) + (IMU_vel.y_vel * trust_value_imu) + (desired_vel.y_vel * trust_value_desired))
	
	

	# Get position according to the encoders
	# Old position plus the new change in position to achieve new position
	pose.theta = state.pose.theta + pose.omega * state.time
	if pose.theta < 0:
		pose.theta = pose.theta + 360
	elif pose.theta > 360:
		pose.theta = pose.theta - 360
	pose.x = state.pose.x + pose.x_vel * state.time
	pose.y = state.pose.y + pose.y_vel * state.time
	
	# # Get position according to the encoders
	# # Old position plus the new change in position to achieve new position
	# encoder_vel.theta = state.pose.theta + encoder_vel.omega * state.time
	# encoder_vel.x = state.pose.x + encoder_vel.x_vel * state.time
	# encoder_vel.y = state.pose.y + encoder_vel.y_vel * state.time
	

	# # Get position according to the IMU
	# # Old position plus the new change in position to achieve new position
	# IMU_vel.theta = state.pose.theta + IMU_vel.omega * state.time
	# IMU_vel.x = state.pose.x + IMU_vel.x_vel * state.time
	# IMU_vel.y = state.pose.y + IMU_vel.y_vel * state.time
	
	# # Get position according to the desired velocity
	# # Old position plus the new change in position to achieve new position
	# desired_vel.theta = state.pose.theta + desired_vel.omega * state.time
	# desired_vel.x = state.pose.x + desired_vel.x_vel * state.time
	# desired_vel.y = state.pose.y + desired_vel.y_vel * state.time


	state.pose = pose
	
	
	# return encoder_vel,IMU_vel,desired_vel
	
	
# def prediction(state, place_recog)

# 	# reference: https://en.wikipedia.org/wiki/Kalman_filter#Extended_Kalman_filter
	
	
# 	locali = [ pose.x_vel ; pose.y_vel ; pose.omega ]
# 	place_recog = [ pose.x_vel ; pose.y_vel ; pose.omega ]
# 	desired = [ pose.x_vel ; pose.y_vel ; pose.omega ]
# 	estimate_c = 
	
# 	#Predicted (a priori) state estimate
# 	#Predicted (a priori) estimate covariance
	
	
	
# 	yk = place_recog - (locali * desired) # Innovation or measurement pre-fit residual
# 	sk = desired * estimate_c * np.transpose(desired)# Innovation (or pre-fit residual) covariance
# 	kk = estimate_c * np.transpose(desired) * sk^-1 # Optimal Kalman gain
# 	xk = locali + kk * yk # Updated (a posteriori) state estimate 
# 	pk = (kk * desired)estimate_c - 1 np.transpose(kk * desired) + kk * np.transpose(kk) # Updated (a posteriori) estimate covariance
# 	ykk = desired * xk # Measurement post-fit residual

	
	
# 	state.pose
	
	
	


	
	