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

img = camera.capture(rawCapture, format='rgb')
cv2.imwrite('img.png', img)

