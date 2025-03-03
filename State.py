import random
import torch
import numpy as np
from Graphics import *

class State:
    def __init__(self, board = None, checkers_eaten = (0, 0), checkers_out = (0, 0),
                  dice = (random.randint(1, 6), random.randint(1, 6)), player = -1, blocked = 0, throw = True):
        if board is not None:
            self.board = board
        else:
            self.board = self.new_board()
        self.checkers_eaten = checkers_eaten
        self.checkers_out = checkers_out
        self.dice = dice
        self.player = player
        self.blocked = blocked
        self.throw = throw
    
    def new_board(self):
        return np.array([2, 0, 0, 0, 0, -5,
                         0, -3, 0, 0, 0, 5,
                         -5, 0, 0, 0, 3, 0,
                         5, 0, 0, 0, 0, -2])

    def copy(self):
        board = self.board.copy()
        white_checkers_eaten, black_checkers_eaten = self.checkers_eaten
        white_checkers_out, black_checkers_out = self.checkers_out
        dice1, dice2 = self.dice
        player = self.player
        blocked = self.blocked
        throw = self.throw
        return State(board, (white_checkers_eaten, black_checkers_eaten), (white_checkers_out, black_checkers_out),
                      (dice1, dice2), player, blocked, throw)
    
    def to_tensor(self):
        board = self.board.copy()
        dice = np.array(self.dice)
        checkers_eaten = np.array(self.checkers_eaten)
        checkers_out = np.array(self.checkers_out)
        tensor = torch.tensor(np.concatenate([board, dice, checkers_eaten, checkers_out]))
        return tensor

    [staticmethod]
    def to_state(state_tensor, player):
        state_tensor = state_tensor.to(torch.int)
        res = State(board = np.array(state_tensor[:24]), dice = (state_tensor[24].item(), state_tensor[25].item()), 
                     checkers_eaten = (state_tensor[26].item(), state_tensor[27].item()),
                     checkers_out = (state_tensor[28].item(), state_tensor[29].item()), player = player)
        return res

    