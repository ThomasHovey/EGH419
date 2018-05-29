import numpy as np
import time
from classes.IMU import IMU
from classes.State import State
from classes.Pose import Pose
import comm

state = State()
# Setup serial 
comm.Serial_init()
print

# Create a new 
#state = State()
##imu = IMU()
time.sleep(2)

comm.IMU_config()

# #Update encodersprint

# comm.updateData(state)
# print
# print("Update data... New data received as below:")
# print("L_Encoder: " + str(state.leftDistance) + \
#       ", R_Encoder: " + str(state.rightDistance))

# print("Ax: " + str(state.IMU.x_accel) + ", Ay: " + str(state.IMU.y_accel) + \
#       ", Gz: " + str(state.IMU.z_gyro))

# ##print("Mx: " + str(state.compass.x_mag) + \
# ##      ", My: " + str(state.compass.y_mag) + \
# ##      ", Mz: " + str(state.compass.z_mag))
# print
# time.sleep(2)

# # Update motorspeed
# state.leftMotorSpeed = 100
# state.rightMotorSpeed = 100
# comm.setMotorSpeed(state)
# print
# time.sleep(2)

# # # Update motorspeed
# # state.leftMotorSpeed = -50
# # state.rightMotorSpeed = 140
# # comm.setMotorSpeed(state)
# # print
# # time.sleep(2)

# # # Update motorspeed
# # state.leftMotorSpeed = 40
# # state.rightMotorSpeed = -100
# # comm.setMotorSpeed(state)
# # print
# # time.sleep(2)

# # # Update motorspeed
# # state.leftMotorSpeed = -120
# # state.rightMotorSpeed = -120
# # comm.setMotorSpeed(state)
# # print
# # time.sleep(2)

# # # Update motorspeed
# # state.leftMotorSpeed = -150
# # state.rightMotorSpeed = -100
# # comm.setMotorSpeed(state)
# # print
# # time.sleep(2)

# # Update encodersprint
# comm.updateData(state)
# print
# print("Update data... New data received as below:")
# print("L_Encoder: " + str(state.leftDistance) + \
#       ", R_Encoder: " + str(state.rightDistance))

# print("Ax: " + str(state.IMU.x_accel) + ", Ay: " + str(state.IMU.y_accel) + \
#        ", Gz: " + str(state.IMU.z_gyro))

# ##print("Mx: " + str(state.compass.x_mag) + \
# ##      ", My: " + str(state.compass.y_mag) + \
# ##      ", Mz: " + str(state.compass.z_mag))
# print
# time.sleep(2)

# # Update motorspeed
# state.leftMotorSpeed = 0
# state.rightMotorSpeed = 0
# comm.setMotorSpeed(state)
# print
# time.sleep(2)