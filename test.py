from Environment import *
from State import *
from DQN_Agent import *
from Human_Agent import *
from Advanced_Random_Agent import *
import numpy as np
import random
import timeit

env = Environment(State(board=np.array(
                        [2, 0, 0, 0, 0, -5,
                         0, -3, 0, 0, 0, 5,
                         -5, 0, 0, 0, 3, 0,
                         5, 0, 0, 0, 0, -2]),
                dice = (4, 2), checkers_eaten = (0, 0), checkers_out = (0, 0), player = -1))

