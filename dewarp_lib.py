from SimpleCV import Camera, VideoStream, Color, Display, Image, VirtualCamera
import cv2
import numpy as np
import time
import re

with open('xmap.txt') as f:
    shape = tuple(int(num) for num in re.findall(r'\d+', f.readline()))
xmap = np.loadtxt('xmap.txt').reshape(shape)

with open('ymap.txt') as f:
    shape = tuple(int(num) for num in re.findall(r'\d+', f.readline()))
ymap = np.loadtxt('ymap.txt').reshape(shape)

# do the unwarping 
def unwarp(img):
    # Remap donut to 360 format
    print xmap
    print ymap
    img = Image(img)
    output = cv2.remap(img.getNumpyCv2(),xmap,ymap,cv2.INTER_LINEAR)
    # Return unwarped image
    return output

