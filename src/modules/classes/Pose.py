class Pose:
	""" Class used to store x y and heading infomation """

	def __init__(self, x, y, theta,x_vel,y_vel,omega):
		self.x = x
		self.y = y
		self.theta = theta
		self.x_vel = x_vel
		self.y_vel = y_vel
		self.omega = omega