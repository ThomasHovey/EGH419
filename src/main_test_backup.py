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
import modules.plotting as plotting
import modules.nav as nav
import modules.localization as localization
import matplotlib.pyplot as plt

time.sleep(0.1)

# Init state
state = State()

# Init serial to arduino
comm.Serial_init()


# Chose mode
text = raw_input("Build database or load existing? (l or b)")  # Python 2

if text == "b":

	##################
	# Build Boundary square
	##################

	desired_pos = Pose(500,0,0,0,0,0)
	# Loop
	state.leftMotorSpeed = 20
	state.rightMotorSpeed = 20
	comm.setMotorSpeed(state)

	old_time = time.time()

	
	while state.pose.x <500  :
		#print("Desired x:" + str(desired_pos.x) + " y:" + str(desired_pos.y))
		#print("Current x:" + str(state.pose.x) + " x:" +str(state.pose.y) + " theta:" + str(state.pose.theta))


		# Read encoder data ect
		comm.updateData(state)
		# Find time 
		state.time = time.time() - old_time
		old_time = time.time()
		# Update localization
		localization.update(state)
		plotting.update_plot(state.pose)

		# Add img to database
		database = place_recog.database_append(state.pose)




	print("Reached Node Point")
	# Stop
	state.leftMotorSpeed = 0
	state.rightMotorSpeed = 0
	comm.setMotorSpeed(state)


	# Plot database locations
	plotting.update_plot(state.pose)
	plotting.add_database(database)

	# Draw Plot
	plotting.draw_plot()

	# Loop
	state.leftMotorSpeed = -10
	state.rightMotorSpeed = 10
	comm.setMotorSpeed(state)

	old_time = time.time()

	
	while state.pose.theta < 90 or state.pose.theta > 180  :
		#print("Desired x:" + str(desired_pos.x) + " y:" + str(desired_pos.y))
		#print("Current x:" + str(state.pose.x) + " x:" +str(state.pose.y) + " theta:" + str(state.pose.theta))


		# Read encoder data ect
		comm.updateData(state)
		# Find time 
		state.time = time.time() - old_time
		old_time = time.time()
		# Update localization
		localization.update(state)
		plotting.update_plot(state.pose)

		# Add img to database
		#database = place_recog.database_append(state.pose)




	print("Reached Node Point")
	# Stop
	state.leftMotorSpeed = 0
	state.rightMotorSpeed = 0
	comm.setMotorSpeed(state)


##################
	# Build Boundary square
	##################

	desired_pos = Pose(500,500,0,0,0,0)
	# Loop
	state.leftMotorSpeed = 20
	state.rightMotorSpeed = 20
	comm.setMotorSpeed(state)

	old_time = time.time()

	
	while state.pose.y <500  :
		#print("Desired x:" + str(desired_pos.x) + " y:" + str(desired_pos.y))
		#print("Current x:" + str(state.pose.x) + " x:" +str(state.pose.y) + " theta:" + str(state.pose.theta))


		# Read encoder data ect
		comm.updateData(state)
		# Find time 
		state.time = time.time() - old_time
		old_time = time.time()
		# Update localization
		localization.update(state)
		plotting.update_plot(state.pose)

		# Add img to database
		database = place_recog.database_append(state.pose)




	print("Reached Node Point")
	# Stop
	state.leftMotorSpeed = 0
	state.rightMotorSpeed = 0
	comm.setMotorSpeed(state)


	# Plot database locations
	plotting.update_plot(state.pose)
	plotting.add_database(database)

	# Draw Plot
	plotting.draw_plot()

	# Loop
	state.leftMotorSpeed = -10
	state.rightMotorSpeed = 10
	comm.setMotorSpeed(state)

	old_time = time.time()

	
	while state.pose.theta < 180  :
		#print("Desired x:" + str(desired_pos.x) + " y:" + str(desired_pos.y))
		#print("Current x:" + str(state.pose.x) + " x:" +str(state.pose.y) + " theta:" + str(state.pose.theta))


		# Read encoder data ect
		comm.updateData(state)
		# Find time 
		state.time = time.time() - old_time
		old_time = time.time()
		# Update localization
		localization.update(state)
		plotting.update_plot(state.pose)

		# Add img to database
		#database = place_recog.database_append(state.pose)




	print("Reached Node Point")
	# Stop
	state.leftMotorSpeed = 0
	state.rightMotorSpeed = 0
	comm.setMotorSpeed(state)

##################
	# Build Boundary square
	##################

	desired_pos = Pose(0,500,0,0,0,0)
	# Loop
	state.leftMotorSpeed = 20
	state.rightMotorSpeed = 20
	comm.setMotorSpeed(state)

	old_time = time.time()

	
	while state.pose.x > 0  :
		#print("Desired x:" + str(desired_pos.x) + " y:" + str(desired_pos.y))
		#print("Current x:" + str(state.pose.x) + " x:" +str(state.pose.y) + " theta:" + str(state.pose.theta))


		# Read encoder data ect
		comm.updateData(state)
		# Find time 
		state.time = time.time() - old_time
		old_time = time.time()
		# Update localization
		localization.update(state)
		plotting.update_plot(state.pose)

		# Add img to database
		database = place_recog.database_append(state.pose)




	print("Reached Node Point")
	# Stop
	state.leftMotorSpeed = 0
	state.rightMotorSpeed = 0
	comm.setMotorSpeed(state)


	# Plot database locations
	plotting.update_plot(state.pose)
	plotting.add_database(database)

	# Draw Plot
	plotting.draw_plot()

	# Loop
	state.leftMotorSpeed = -10
	state.rightMotorSpeed = 10
	comm.setMotorSpeed(state)

	old_time = time.time()

	
	while state.pose.theta < 270  :
		#print("Desired x:" + str(desired_pos.x) + " y:" + str(desired_pos.y))
		#print("Current x:" + str(state.pose.x) + " x:" +str(state.pose.y) + " theta:" + str(state.pose.theta))


		# Read encoder data ect
		comm.updateData(state)
		# Find time 
		state.time = time.time() - old_time
		old_time = time.time()
		# Update localization
		localization.update(state)
		plotting.update_plot(state.pose)

		# Add img to database
		#database = place_recog.database_append(state.pose)




	print("Reached Node Point")
	# Stop
	state.leftMotorSpeed = 0
	state.rightMotorSpeed = 0
	comm.setMotorSpeed(state)

##################
	# Build Boundary square
	##################

	desired_pos = Pose(0,0,0,0,0,0)
	# Loop
	state.leftMotorSpeed = 20
	state.rightMotorSpeed = 20
	comm.setMotorSpeed(state)

	old_time = time.time()

	
	while state.pose.y >0  :
		#print("Desired x:" + str(desired_pos.x) + " y:" + str(desired_pos.y))
		#print("Current x:" + str(state.pose.x) + " x:" +str(state.pose.y) + " theta:" + str(state.pose.theta))


		# Read encoder data ect
		comm.updateData(state)
		# Find time 
		state.time = time.time() - old_time
		old_time = time.time()
		# Update localization
		localization.update(state)
		plotting.update_plot(state.pose)

		# Add img to database
		database = place_recog.database_append(state.pose)




	print("Reached Node Point")
	# Stop
	state.leftMotorSpeed = 0
	state.rightMotorSpeed = 0
	comm.setMotorSpeed(state)


	# Plot database locations
	plotting.update_plot(state.pose)
	plotting.add_database(database)

	# Draw Plot
	plotting.draw_plot()

	# Loop
	state.leftMotorSpeed = -10
	state.rightMotorSpeed = 10
	comm.setMotorSpeed(state)

	old_time = time.time()

	
	while state.pose.theta < 360 and state.pose.theta > 100  :
		#print("Desired x:" + str(desired_pos.x) + " y:" + str(desired_pos.y))
		#print("Current x:" + str(state.pose.x) + " x:" +str(state.pose.y) + " theta:" + str(state.pose.theta))


		# Read encoder data ect
		comm.updateData(state)
		# Find time 
		state.time = time.time() - old_time
		old_time = time.time()
		# Update localization
		localization.update(state)
		plotting.update_plot(state.pose)

		# Add img to database
		#database = place_recog.database_append(state.pose)




	print("Reached Node Point")
	# Stop
	state.leftMotorSpeed = 0
	state.rightMotorSpeed = 0
	comm.setMotorSpeed(state)


	


	# Finalize database
	database = place_recog.database_finalize()

else :
	database = place_recog.load_database()
	for data in database:
		print('x: ' + str(data.pose.x))
		print('y: ' + str(data.pose.y))
		print('theta: ' + str(data.pose.theta))

# Draw plot
plotting.add_database(database)
plotting.draw_plot()


#################
# Move to position
#################
# Set target

target_pose = Pose(800,400,0,0,0,0)

print(target_pose.x)
print(target_pose.y)	

## Now database is loaded 
text = raw_input("Ready to start mowing?")

# Loop
old_time = time.time()

while abs(state.pose.x - target_pose.x) > 50 or abs(state.pose.y - target_pose.y) > 50  :
	
	# Read encoder data ect
	comm.updateData(state)
	# Find time 
	state.time = time.time() - old_time
	old_time = time.time()
	# Update localization
	localization.update(state)

	# Update plot
	plotting.update_plot(state.pose)
	if state.pose.x > 50 and state.pose.y > 50:
	# Check place recognition
		pose, error = place_recog.find_location(state.pose)
		if error != 'NULL':
			plotting.update_plot_img(state.pose)
			print("match found: error: " + str(error) )
			print("Posex: " + str(pose.x))
			print("Posey: " + str(pose.y))
			state.pose.x = pose.x
			state.pose.y = pose.y
			if state.pose.x > 250 and state.pose.y > 250:
				break
		else:
			print("No image matched")

	# Get motor speeds and update
	nav.moveToPoint(state, target_pose)
	comm.setMotorSpeed(state)



# Stop
state.leftMotorSpeed = 0
state.rightMotorSpeed = 0
comm.setMotorSpeed(state)

# Draw Plot
plotting.draw_plot()

while(1):
	time.sleep(1)