import numpy as np
import time
from classes.State import State
from classes.Pose import Pose
import localization

state = State()

# Add distance
state.LeftDistance = 10.0
state.RightDistance = 15.0 
state.Time = 1.0


localization.map_encoder(state)

print("X pos: " )
print( state.Pose.x )
print( " Y Pos: ")
print( state.Pose.y )
print( " Theta: " )
print(state.Pose.theta)