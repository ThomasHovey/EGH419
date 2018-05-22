import numpy as np
import time
from classes.IMU import IMU
from classes.State import State
from classes.Pose import Pose
import comm


# Setup serial 
comm.Serial_init()
print

# Create a new 
state = State()
##imu = IMU()
time.sleep(2)

# Update encodersprint

comm.updateData(state)
print
print("Update data... New data received as below:")
print("L_Encoder: " + str(state.LeftDistance) + \
      ", R_Encoder: " + str(state.RightDistance))

print("Ax: " + str(state.IMU.x_accel) + ", Ay: " + str(state.IMU.y_accel) + \
      ", Az: " + str(state.IMU.z_accel) + ", Gx: " + str(state.IMU.x_gyro) + \
      ", Gy: " + str(state.IMU.y_gyro) + ", Gz: " + str(state.IMU.z_gyro))

print("Mx: " + str(state.Compass.x_mag) + \
      ", My: " + str(state.Compass.y_mag) + \
      ", Mz: " + str(state.Compass.z_mag))
print
time.sleep(5)

# Update motorspeed
state.LeftMotorSpeed = 100
state.RightMotorSpeed = 100
comm.setMotorSpeed(state)
print
time.sleep(5)

# Update motorspeed
state.LeftMotorSpeed = -50
state.RightMotorSpeed = 140
comm.setMotorSpeed(state)
print
time.sleep(5)

# Update motorspeed
state.LeftMotorSpeed = 40
state.RightMotorSpeed = -100
comm.setMotorSpeed(state)
print
time.sleep(5)

# Update motorspeed
state.LeftMotorSpeed = -120
state.RightMotorSpeed = -120
comm.setMotorSpeed(state)
print
time.sleep(5)

# Update motorspeed
state.LeftMotorSpeed = -150
state.RightMotorSpeed = -100
comm.setMotorSpeed(state)
print
time.sleep(5)

# Update encodersprint
comm.updateData(state)
print
print("Update data... New data received as below:")
print("L_Encoder: " + str(state.LeftDistance) + \
      ", R_Encoder: " + str(state.RightDistance))

print("Ax: " + str(state.IMU.x_accel) + ", Ay: " + str(state.IMU.y_accel) + \
      ", Az: " + str(state.IMU.z_accel) + ", Gx: " + str(state.IMU.x_gyro) + \
      ", Gy: " + str(state.IMU.y_gyro) + ", Gz: " + str(state.IMU.z_gyro))

print("Mx: " + str(state.Compass.x_mag) + \
      ", My: " + str(state.Compass.y_mag) + \
      ", Mz: " + str(state.Compass.z_mag))
print
time.sleep(5)

# Update motorspeed
state.LeftMotorSpeed = 0
state.RightMotorSpeed = 0
comm.setMotorSpeed(state)
print
time.sleep(2)
