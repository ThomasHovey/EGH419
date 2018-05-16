import Pose

class State:

	def __init__(self, ):
		self.LeftMotorSpeed = 0
		self.RightMotorSpeed = 0
		self.LeftEncoder = 0
		self.RightEncoder = 0
		self.IMU = []
		self.Compass = []
		self.Pose = Pose(0,0,0)