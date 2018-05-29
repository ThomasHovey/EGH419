import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera 
import time
from classes.Pose import Pose
from classes.ImageData import ImageData
from classes.State import State

# Tuning Constants
POSE_TOLERANCE = 100
ERROR_THRESHOLD = 10.0
# Empty database
database = []

# Setup camera
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 30
#Wait
time.sleep(1.0)
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

rawCapture = PiRGBArray(camera)

# Import map for unwrapping 360 image
xmap = np.load("modules/data/xmap.npy")
ymap = np.load("modules/data/ymap.npy")

time.sleep(0.1)

def get_img():
	# Capture Image
	camera.capture(rawCapture, format='rgb')
	# Convert to CV2 img
	img = rawCapture.array
	# Convert to grayscale
	img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#Dewarp
	output = cv2.remap(img_gray,xmap,ymap,cv2.INTER_LINEAR)
	rawCapture.truncate(0) 
	# Resize TODO
	return output



def find_location(pose):
	# Search the data base for images that are close to the current estimated location
	img = get_img()
	database_temp = []
	for data in database:
		if (pose.x - data.pose.x < POSE_TOLERANCE and pose.x - data.pose.x > -POSE_TOLERANCE) \
		and (pose.y - data.pose.y < POSE_TOLERANCE and pose.y - data.pose.y > -POSE_TOLERANCE):
			database_temp.append(data)
	database_temp = database
	
	# Return null if not close to boundary
	if database_temp == []:
		return Pose(0,0,0,0,0,0), 'NULL'

	# Check database	
	else:
		# Search the close images for one that matches our location
		error_database = []
		for data in database_temp:
			# Get the difference
			img_diff = abs(img.astype(int) - data.img.astype(int))
			img_diff = np.array(img_diff,dtype = np.uint8)
			
			# Find the avg error
			error = np.mean(img_diff)

			# Check if error is below threshold
			if error < ERROR_THRESHOLD:
				error_database.append((error, data.pose))

			im_stack = np.vstack((data.img,img))
			im_stack = np.vstack((im_stack, img_diff))
			cv2.imshow("Database img, current image, difference", im_stack)
			#print("Error is " + str(error))	
			cv2.waitKey(1)

		# Return null if no matches
		if error_database == []:
			return Pose(0,0,0,0,0,0), 'NULL'
		# Else return best match
		else:
			error_database.sort(key=lambda tup: tup[0])
			return (error_database[0][1], error_database[0][0])

def build_database_old():
	database = []
	while 1:
		key = raw_input("Enter pose x value (press e to finish)")
		if key == 'E' or key == 'e':
			np.save('modules/data/database.npy',database)
			return database
		pose = Pose(int(key),0,0,0,0,0)
		capture = get_img()
		database.append(ImageData(capture,pose))
		#cv2.imwrite('img.png',capture)

def database_append(state):
	capture = get_img()
	database.append(ImageData(capture,state.pose))
	#cv2.imwrite('img.png',capture)
	return database

def database_finalize():
	np.save('modules/data/database.npy',database)
	return database
	

def load_database():
	database = np.load('modules/data/database.npy')
	return database



# # Build database
# database = build_database()

# # Setup current location
# pose_current = class_info.Pose(1.5,0,0)

# while 1:
# 	# When ready capture an image
# 	# key = raw_input("Enter any key to check (e or E to exit)")
# 	# if key == 'E' or key == 'e':
# 	# 	break
# 	capture = get_image()

# 	# Image search for closest image
# 	new_pose, error = find_location(capture, database, pose_current)

# 	# Print answer
# 	print("Pos : " + str(new_pose.x) + " Error : " + str(error))

# Close camera
	



#######################################################################################
############                       CODE CEMETARY                         ##############

#load images
# im_1 =cv2.resize(cv2.imread('test1.jpg', 0), (320,320))
# im_2 =cv2.resize(cv2.imread('test2.jpg', 0), (320,320))
# im_3 =cv2.resize(cv2.imread('test3.jpg', 0), (320,320))

# database is a list of image objects  
# database = []
# database.append(class_info.ImageData(im_1, class_info.Pose(1,0,0)))
# database.append(class_info.ImageData(im_2, class_info.Pose(2,0,0)))
