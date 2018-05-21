import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera 
import time

# Setup camera
camera = PiCamera()
camera.resolution = (1312,972)
camera.framerate = 30
#Wait
time.sleep(1.0)
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

rawCapture = PiRGBArray(camera)

time.sleep(0.1)

camera.capture(rawCapture, format='rgb')
cv2.imwrite('img.png', rawCapture)

