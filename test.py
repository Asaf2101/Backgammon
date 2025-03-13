from Environment import *
from State import *
from DQN_Agent import *
from Human_Agent import *
from Advanced_Random_Agent import *
import numpy as np
import random
import timeit

env = Environment(State(board=np.array(
                        [0, -13, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0,
                         1, 11, 2, 0, 1, 0]),
                dice = (4, 2), checkers_eaten = (0, 2), checkers_out = (0, 0), player = -1))


actions = env.get_all_actions(state = env.state)
# print('all actions:', actions)
print('------------------------------------------------')
action = random.choice(actions)
print('action', action)
print('------------------------------------------------')
print('reward1:', env.move(action[0]))
print('reward2:', env.move(action[1]))
