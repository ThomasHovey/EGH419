import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera 
import time
from classes.Pose import Pose
from classes.ImageData import ImageData


# Tuning Constants
POSE_TOLERANCE = 10

# Setup camera
camera = PiCamera()
camera.resolution = (1296,972)
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
xmap = np.load('data/xmap.npy')
ymap = np.load('data/ymap.npy')

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

	# Resize TODO
	return output

# Captures a single image from the camera and returns it in PIL format
def get_image():
	# read is the easiest way to get a full image out of a VideoCapture object.
	camera = cv2.VideoCapture(camera_port)
	retval, im = camera.read()
	im = cv2.resize(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY),(320,240))
	del(camera)	
	return im

def find_location(img, database, pose):
	# Search the data base for images that are close to the current estimated location
	database_temp = []
	for data in database:
		if (pose.x - data.pose.x < POSE_TOLERANCE and pose.x - data.pose.x > -POSE_TOLERANCE) \
		and (pose.y - data.pose.y < POSE_TOLERANCE and pose.y - data.pose.y > -POSE_TOLERANCE):
			database_temp.append(data)
	# Search the close images for one that matches our location
	error_database = []
	for data in database_temp:
		img_diff = abs(img.astype(int) - data.img.astype(int))
		img_diff = np.array(img_diff,dtype = np.uint8)
		
		error = np.mean(img_diff)
		error_database.append((error, data.pose))

		im_stack = np.hstack((data.img,img))
		im_stack = np.hstack((im_stack, img_diff))
		cv2.imshow("Database img, current image, difference", im_stack)
		#print("Error is " + str(error))	
		cv2.waitKey(100)
	# Use the pose with the lowest error
	
	# cv2.destroyAllWindows()
	error_database.sort(key=lambda tup: tup[0])
	return (error_database[0][1], error_database[0][0])

def build_database():
	database = []
	while 1:
		key = raw_input("Enter pose x value (press e to finish)")
		if key == 'E' or key == 'e':
			np.save('data/database.npy',np.asarray(database))
			return database
		pose = class_info.Pose(int(key),0,0)
		capture = get_image()
		database.append(class_info.ImageData(capture,pose))
		cv2.imwrite('img.png',capture)

def load_database():
	database = np.load('data/database.npy')
	database.toList()
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
