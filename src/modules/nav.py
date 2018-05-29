import numpy as np
from classes.State import State
from classes.Pose import Pose
import math

Kv = 0.15
Kh = 0.03 # 0.015
W = 100.0
Kh_t = 9

def moveToPoint(state,desired_pose):
	v = Kv*math.sqrt(math.pow(min(120,max(80,desired_pose.x - state.pose.x)),2) + math.pow(min(120,max(80,desired_pose.y - state.pose.y)),2))
	desired_theta = math.atan2(desired_pose.y - state.pose.y,desired_pose.x - state.pose.x)*(180/math.pi)
	steering_diff = desired_theta - state.pose.theta

	if steering_diff > 180:
		steering_diff = steering_diff - 360
	elif steering_diff < -180:
		steering_diff = steering_diff +360
	steering_angle = Kh*(steering_diff)*(math.sqrt(math.pow(min(100,desired_pose.x - state.pose.x),2) + math.pow(min(100,desired_pose.y - state.pose.y),2)))/200
	if steering_angle > 0.25:
		v = 0
		steering_angle = 0.15
	elif steering_angle < -0.25:
		v = 0
		steering_angle = -0.15

	l_motor = v - steering_angle*W/2
	r_motor = steering_angle*W + l_motor


	l_motor = int(min(140,max(-140,l_motor)))
	r_motor = int(min(140,max(-140,r_motor)))
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
