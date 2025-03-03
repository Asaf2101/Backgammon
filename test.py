from Environment import *
from State import *
from DQN_Agent import *
from Human_Agent import *
import numpy as np
import timeit
import sys

env = Environment(State(board=np.array([0, 0, 0, 0, 0, -5,
                                         0, -4, -4, 0, 0, 0,
                                        0, 0, 0, 0, 8, 5,
                                        2, 0, 0, 0, 0, -2]), dice = (5, 3), checkers_eaten = (0, 0), checkers_out=(0, 0), player = 1))

print('res0:', env.slow_get_all_actions())
print('------------------------------------------------')
print('res2:', env.get_all_actions(state = env.state))


# iterations = 1000
# time_method_1 = timeit.timeit(env.slow_get_all_actions, number = iterations)
# time_method_2 = timeit.timeit(lambda: env.get_all_actions(env.state), number = iterations)

# print(f"Method 1 took: {time_method_1} seconds. ({iterations} iterations)")
# print(f"Method 2 took: {time_method_2} seconds. ({iterations} iterations)")
# print(time_method_1 / time_method_2)
