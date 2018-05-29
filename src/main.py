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
import threading, time, sys
import pygame

# teleop constant
FORWARD = 'w'
LEFT = 'a'
RIGHT = 'd'
REVERSE = 's'
FINISH = 'f'
STOP = 'v'
# Pause
time.sleep(0.1)

# Init state
state = State()

# Init serial to arduino
comm.Serial_init()

key = "lol"

pygame.init()
pygame.display.set_mode((200,200))


lock = threading.Lock()

def thread_teleop():
	global key
	while True:
		lock.acquire()
		key = STOP
		pygame.event.get()
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_a]:
			key = 'a'
		elif pressed[pygame.K_w]:
			key = 'w'
		elif pressed[pygame.K_s]:
			key = 's'
		elif pressed[pygame.K_d]:
			key = 'd'
		elif pressed[pygame.K_f]:
			key = 'f'
		
		if key == FINISH:
			lock.release()
			print("Exit thread1")
			sys.exit()
		lock.release()
		time.sleep(0.01)


def main_build_database():
	old_time = time.time()
	while key != FINISH:
		# Read encoder data ect
		comm.updateData(state)
		# Find time 
		state.time = time.time() - old_time
		old_time = time.time()
		# Update localization
		localization.update(state)

		if state.leftMotorSpeed != 0 or state.rightMotorSpeed !=0:

			# Add img to database
			database = place_recog.database_append(state)
			# Plot database locations
			plotting.add_database(database)


		# Update plot
		plotting.update_plot(state.pose)


		while True:
			acquired = lock.acquire(0)
			if acquired:
				break
		# Get motor speeds from teleop
		if key == FORWARD:
			state.leftMotorSpeed = 15
			state.rightMotorSpeed = 15
		elif key == REVERSE:
			state.leftMotorSpeed = -15
			state.rightMotorSpeed = -15
		elif key == LEFT:
			state.leftMotorSpeed = -15
			state.rightMotorSpeed = 15
			comm.setMotorSpeed(state)
			time.sleep(0.1)
			state.leftMotorSpeed = 0
			state.rightMotorSpeed = 0
			comm.setMotorSpeed(state)
			
		elif key == RIGHT:
			state.leftMotorSpeed = 15
			state.rightMotorSpeed = -15
			comm.setMotorSpeed(state)
			time.sleep(0.1)
			state.leftMotorSpeed = 0
			state.rightMotorSpeed = 0
			comm.setMotorSpeed(state)
		else:
			state.leftMotorSpeed = 0
			state.rightMotorSpeed = 0

		lock.release()
		comm.setMotorSpeed(state)

		time.sleep(0.01)

	print("Exit thread main")
#	sys.exit()
		
##################################
# START
##################################



# Chose mode
text = raw_input("Build database or load existing? (l or b)")  # Python 2

if text == "b":
		
	threading.Thread(target = thread_teleop).start()
	main_build_database()

	#while key != FINISH:
	plotting.plotting_main()


	# Finalize database
	database = place_recog.database_finalize()

else :
	database = place_recog.load_database()




## Now database is loaded 
text = raw_input("Ready to start mowing?")

# Loop
old_time = time.time()

# Set target
target_pose = database[len(database)/2].pose
	
i=0

while abs(state.pose.x - target_pose.x) < 20 or abs(state.pose.y - target_pose.y) < 20:
	
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)

	# Update plot
	plotting.update_plot()
	
	# Check place recognition
	pose, error = place_recog.find_location()
	if error != 'NULL'
		plotting.add_img_found(pose,error)
		state.pose.x = pose.x
		state.pose.y = pose.y
	else:
		print("No image matched")

	# Get motor speeds and update
	nav.moveToPoint(state, target_pose)
	comm.setMotorSpeed(state)
	if i == 10:
		plotting.draw_plot(state.pose)


# Stop
state.leftMotorSpeed = 0
state.rightMotorSpeed = 0
comm.setMotorSpeed(state)

# Draw Plot
plotting.draw_plot(state.pose)
