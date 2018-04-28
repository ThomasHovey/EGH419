class ImageData:
	""" Class used to store image files, along with the pose """

	def __init__(self, img, pose):
		self.img = img
		self.pose = pose

class Pose:
	""" Class used to store x y and heading infomation """

	def __init__(self, x, y, theta):
		self.x = x
		self.y = y
		self.theta = theta
		