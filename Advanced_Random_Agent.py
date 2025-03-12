import pygame
import random
from Graphics import *
from Environment import *

class Advanced_Random_Agent:
    def __init__(self, player, env : Environment, graphics : Graphics = None):
        self.player = player
        self.env = env
        self.graphics = graphics
    
    def get_action(self, events = None, state = None, train = False):
        if self.graphics is not None:
            self.graphics(self.env.state)
        # pygame.time.delay(1500)

        actions = self.env.get_all_actions(self.env.state)
        filtered_actions = [a for a in actions
                            if self.is_eat_action(a) or self.is_out_action(a) or self.is_enter_home_action(a)]

        if filtered_actions:
            action = random.choice(filtered_actions)
            # print('smart choice', action)
            return action
        else:
            action = random.choice(actions)
            # print('regular choice', action)
            return action
    
    def is_eat_action(self, action):
        player = self.env.state.player
        board = self.env.state.board
        move1, move2 = action[0], action[1]

        if move1[1] != -1 and move1[1] != 26 and move1[1] != 27:
            if board[move1[1]] == -1 * player: return True
        if move2[1] != -1 and move2[1] != 26 and move2[1] != 27:
            if board[move2[1]] == -1 * player: return True
        
        return False

    def is_out_action(self, action):
        player = self.env.state.player
        move1, move2 = action[0], action[1]

        if player == -1:
            if move1[1] == 26 or move2[1] == 26: return True
        else:
            if move1[1] == 27 or move2[1] == 27: return True
        
        return False

    def is_enter_home_action(self, action):
        player = self.env.state.player
        move1, move2 = action[0], action[1]

        if player == -1:
            if move1[1] != -1:
                if 0 <= move1[1] <= 5 and move1[0] >= 6: return True
            if move2[1] != -1:
                if 0 <= move2[1] <= 5 and move2[0] >= 6: return True
        else:
            if move1[1] != -1:
                if 18 <= move1[1] <= 23 and move1[0] <= 17: return True
            if move2[1] != -1:
                if 18 <= move2[1] <= 23 and move2[0] <= 17: return True
        
        return False
    
