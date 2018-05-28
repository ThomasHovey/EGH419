from Pose import Pose
from IMU import IMU

class State:

	def __init__(self, ):
		self.leftMotorSpeed = 0
		self.rightMotorSpeed = 0
		self.leftDistance = 0
		self.rightDistance = 0
		self.IMU = IMU(0,0,0)
		self.pose = Pose(0,0,0,0,0,0)
		self.time = 0