import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera 
import time

# Setup PiCamera
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


while (1):
	img = get_img()
	cv2.imshow('ShowImg',img)
	cv2.waitKey(0)
	rawCapture.truncate(0) 

