import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera 
import time
import modules.place_recog as place_recog
from modules.classes.Pose import Pose
from modules.classes.ImageData import ImageData
from modules.classes.State import State
import modules.plotting as plotting
import modules.comm as comm
import modules.localization as localization
import matplotlib.pyplot as plt
import math

# Pause
time.sleep(0.1)

# Init state
state = State()

# Init serial to arduino
comm.Serial_init()
plotting.init_plot()

# Chose mode
text = raw_input("Build database or load existing? (load or build)")  # Python 2

if text == "build"
		place_recog.make_database(state)

else :
	place_recog.load_database()

text = raw_input("Ready to start mowing?")

# Loop
old_time = time.time()
while 1:

	
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.Time = time.time() - old_time
	old_time = time.time()
	# Update localization
	encoder,IMU,desired = localization.update(state)

	# Update plot
	plotting.update_plot(state.Pose, encoder, IMU, desired)

	i += 1

# Stop
state.LeftMotorSpeed = 0
state.RightMotorSpeed = 0
comm.setMotorSpeed(state)

# Draw Plot
plotting.draw_plot(state.Pose, encoder, IMU, desired)
