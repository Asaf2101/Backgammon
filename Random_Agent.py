import pygame
import random
from Graphics import *
from Environment import *

class Random_Agent:
    def __init__(self, player, env : Environment, graphics : Graphics = None):
        self.player = player
        self.env = env
        self.graphics = graphics

    def get_action(self, events = None, state = None, train = False):
        if self.graphics is not None:
            self.graphics(self.env.state)
        # pygame.time.delay(1500)

        actions = self.env.get_all_actions(self.env.state)
        action = random.choice(actions)
         
        return action
        
    