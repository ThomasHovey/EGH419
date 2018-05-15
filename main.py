import cv2
import numpy as np
#import dewarp_lib
from picamera.array import PiRGBArray
from picamera import PiCamera 
import time

# Setup PiCamera
camera = PiCamera()
camera.resolution = (340,120)
camera.framerate = 30
#Wait
time.sleep(2.0)
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

rawCapture = PiRGBArray(camera)


time.sleep(0.1)

def get_img():
	# Capture Image
	camera.capture(rawCapture, format='rgb')
	# Convert to CV2 img
	img = rawCapture.array
	# Convert to grayscale
	img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	return img_gray


while (1):
	img = get_img()
	cv2.imshow('ShowImg',img)
	cv2.waitKey(20)
	rawCapture.truncate(0) 

