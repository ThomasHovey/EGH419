import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera 
import time
import modules.place_recog as place_recog
from modules.classes.Pose import Pose
from modules.classes.ImageData import ImageData
import modules.comm as comm
import modules.localization as localization


time.sleep(0.1)


	
# Build database
database = place_recog.build_database()

database_new = place_recog.load_database()

if database == database_new:
	print("Database loaded correctly\n")
else:
	print("Database load failed\n")

# Setup current location
pose_current = Pose(1.5,0,0,0,0,0)

while 1:
	# When ready capture an image
	# key = raw_input("Enter any key to check (e or E to exit)")
	# if key == 'E' or key == 'e':
	# 	break
	capture = place_recog.get_image()

	# Image search for closest image
	new_pose, error = place_recog.find_location(capture, database, pose_current)

	# Print answer
	print("Pos : " + str(new_pose.x) + " Error : " + str(error))




