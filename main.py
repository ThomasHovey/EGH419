import cv2
import numpy as np
import dewarp_lib
from picamera.array import PiRGBArray
from picamera import PiCamera 
import time

# Setup PiCamera
camera = PiCamera()
rawCapture = PiRGBArray(camera)

time.sleep(0.1)

def get_img():
	camera.capture(rawCapture, format='gray')
	img = rawCapture.array

	return img


while (1):
	img = get_img()
	cv2.imshow(img)
	cv2.waitKey(0)

	