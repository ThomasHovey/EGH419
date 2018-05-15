# EGH419

v3_0 - Updating for vision code to run on the PI

class_info.py contains all the classes used in this project. 

place_recog.py is the second version of our place recognition algorithm. It will build a data base of images, you give each image a x coord as you input it. Then once you build the database you can then take another photo and compare it to those in the data base already. Fairly robust system. You will need open cv installed and it uses your webcam. 

dewarp_build_maps.py is the dewarping alogrithm used to build a xmap and ymap to unwrap 360degree images.

dewarp_lib.py contains the functions to dewarp the 360 degree image on the pi. NOT YET COMPLETED

main.py is the main script on the PI. NOT YET COMPLETED

PiToArduino.py 

ArduinoToPi.ino
