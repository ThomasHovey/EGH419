import cv2
import numpy as np
import dewarp_lib

im_1 =cv2.imread('img4.jpg', 0)
img = dewarp_lib.unwarp(im_1)
print img.size
cv2.imshow(img)
cv2.waitKey(0)