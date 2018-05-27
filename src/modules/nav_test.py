import numpy as np
from classes.State import State
from classes.Pose import Pose
import nav
import math

state= State()

desired = Pose(300,300,0,0,0,0)

nav.moveToPoint(state,desired)