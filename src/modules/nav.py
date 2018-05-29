import numpy as np
from classes.State import State
from classes.Pose import Pose
import math

Kv = 0.5
Kh = 0.006 # 0.015
W = 150.0
diff_gain = 0.2
Kh_t = 9

def moveToPoint(state,desired_pose):
	#v = Kv*math.sqrt(math.pow(min(200,max(80,desired_pose.x - state.pose.x)),2) + math.pow(min(200,max(80,desired_pose.y - state.pose.y)),2))
	desired_theta = math.atan2(desired_pose.y - state.pose.y,desired_pose.x - state.pose.x)*(180/math.pi)
	if desired_theta < 0:
		desired_theta = desired_theta + 360
	# print("desired_theta" + str(desired_theta))
	# print("state.pose.theta" + str(state.pose.theta))

	steering_diff = desired_theta - state.pose.theta
	#print(steering_diff)
	v = min(12,Kv*(math.sqrt(math.pow(min(300,max(90,abs(desired_pose.x - state.pose.x))),2) + \
		math.pow(min(300,max(90,abs(desired_pose.y - state.pose.y))),2)))/abs(max(0.01,steering_diff*diff_gain)))
	#print(v)
	if steering_diff > 180:
		steering_diff = steering_diff - 360
	elif steering_diff < -180:
		steering_diff = steering_diff +360
	steering_angle = Kh*(steering_diff)*(math.sqrt(math.pow(min(100,abs(desired_pose.x - state.pose.x)),2) + math.pow(min(100,abs(desired_pose.y - state.pose.y)),2)))/200
	
	# if steering_angle > 0.15:
	# 	v = 0
	# 	steering_angle = 0.15
	# elif steering_angle < -0.15:
	# 	v = 0
	# 	steering_angle = -0.15

	# print("Steering_angle : " + str(steering_angle))
	l_motor = v - steering_angle*W/2
	r_motor = steering_angle*W + l_motor

	if l_motor < -0:
		l_motor = int(min(-8,max(-20,l_motor)))
	elif l_motor > 0:
		l_motor = int(max(8,min(20,l_motor)))
	else:
		l_motor = 0
	if r_motor < -0:
		r_motor = int(min(-8,max(-20,r_motor)))
	elif r_motor > 0:
		r_motor = int(max(8,min(20,r_motor)))
	else:
		r_motor = 0
	# print("l_motor" + str(l_motor))
	# print("r_motor"+str(r_motor))
	state.leftMotorSpeed = l_motor
	state.rightMotorSpeed = r_motor

def turnToHeading(state, new_heading):
	v = 0
	steering_angle = Kh_t*(new_heading-state.pose.theta)

	l_motor = v - 1/2 * steering_angle * W
	r_motor = steering_angle * W+ l_motor
	
	l_motor = min(140,max(-140,l_motor))
	r_motor = min(140,max(-140,r_motor))
	
	state.leftMotorSpeed = l_motor
	state.rightMotorSpeed = r_motor
