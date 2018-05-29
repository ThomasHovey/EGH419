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
from modules.plotting import draw_plot_thread
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

# Init state
state = State()

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


def main():
	old_time = time.time()
	while key != FINISH:
		# Read encoder data ect
		#comm.updateData(state)
		# Find time 
		state.time = time.time() - old_time
		old_time = time.time()
		# Update localization
		localization.update(state)

		# Add img to database
		place_recog.database_append(state)

		# Update plot
		plotting.update_plot(state.pose)

		# Plot database locations
		plotting.add_database(database)

		while True:
			acquired = lock.acquire(0)
			if acquired:
				break
		# Get motor speeds from teleop
		if key == FORWARD:
			state.leftMotorSpeed = 25
			state.rightMotorSpeed = 25
		elif key == REVERSE:
			state.leftMotorSpeed = -25
			state.rightMotorSpeed = -25
		elif key == LEFT:
			state.leftMotorSpeed = -20
			state.rightMotorSpeed = 20

		elif key == RIGHT:
			state.leftMotorSpeed = 20
			state.rightMotorSpeed = -20

		else:
			state.leftMotorSpeed = 0
			state.rightMotorSpeed = 0

		lock.release()
		time.sleep(0.2)
		comm.setMotorSpeed(state)

	print("Exit thread main")
	sys.exit()

def thread_plot():
	while(1):
		time.sleep(0.5)
		plotting.draw_plot_thread()
		if key == FINISH:
			print("Exit thread Plotting")
			sys.exit()

		

threading.Thread(target = thread_teleop).start()
#threading.Thread(target = thread_plot).start()
threading.Thread(target = main).start()

plotting.plotting_main()






