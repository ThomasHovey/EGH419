import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera 
import time
import modules.place_recog as place_recog
from modules.classes.Pose import Pose
from modules.classes.ImageData import ImageData
from modules.classes.State import State
import modules.comm as comm
import modules.localization as localization

import math
# while(1):
# 	img = place_recog.get_img(0)
# 	cv2.imshow('img', img)
# 	cv2.waitKey(100)

 
# Init state
state = State()

# Init serial to arduino
comm.Serial_init()

old_time = time.time()

while 1:
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)

	# Update plot
	#plotting.update_plot(state.pose)
	print(state.pose.theta)
	# Nav 
	img = place_recog.get_img(state.pose.theta)
	cv2.imshow('img', img)
	cv2.waitKey(100)
