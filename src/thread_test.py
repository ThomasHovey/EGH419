import readchar
import threading, time, sys
import pygame
import modules.plotting as plotting
import modules.comm as comm
import modules.localization as localization
import matplotlib.pyplot as plt


STOP = 'v' 
FINISH = 'f'
key = "lol"

pygame.init()
pygame.display.set_mode((200,200))

lock = threading.Lock()

def thread1():
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
			sys.exit()
			print("Exit thread")
		lock.release()
		time.sleep(0.01)

threading.Thread(target = thread1).start()

while (1):
	
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
		#place_recog.database_append(state)

		# Update plot
		plotting.update_plot(state.Pose)

		# Plot database locations
		#plotting.add_database(database)

		while not acquired:
			acquired = lock.acquire(0)
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
		
		#comm.setMotorSpeed(state)






		lock.release()
	