import cv2
import numpy as np
#from picamera.array import PiRGBArray
#from picamera import PiCamera 
import time
import modules.place_recog as place_recog
from modules.classes.Pose import Pose
from modules.classes.ImageData import ImageData


time.sleep(0.1)

def setup():
	place_recog.setup()

while (1):
	img = place_recog.get_img()
	cv2.imshow('ShowImg',img)
	cv2.waitKey(0)
	rawCapture.truncate(0) 

