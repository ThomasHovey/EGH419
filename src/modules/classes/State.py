from Pose import Pose
class State:

	def __init__(self, ):
		self.LeftMotorSpeed = 0
		self.RightMotorSpeed = 0
		self.LeftDistance = 0
		self.RightDistance = 0
		self.IMU = []
		self.Compass = []
		self.Pose = Pose(0,0,0)
		self.Time = 0.0