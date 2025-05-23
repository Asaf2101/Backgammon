from Environment import Environment
from State import State
from Human_Agent import Human_Agent
from Random_Agent import Random_Agent
from DQN_Agent import DQN_Agent
from Advanced_Random_Agent import Advanced_Random_Agent
from Diverse_Agent import Diverse_Agent
import torch
import random

# path = 'Data/Player1/Model-test5.pth'
# checkpoint = torch.load('Data/Player1/checkpoint-test5.pth')
# env = Environment()
# player1 = DQN_Agent(1, env = env, train = False)
# player1.DQN.load_state_dict(checkpoint['best_model_state_dict'])
# print(checkpoint['best_win_precentage'])
# player2 = Random_Agent(2, env = env, graphics = None)

class Tester:
    def __init__(self, env : Environment, player1, player2):
        self.env = env
        self.player1 = player1
        self.player2 = player2
    
    def test(self, games_num):
        black_win, white_win = 0, 0
        for game in range(games_num):
            print('game =', game, end = '\r')

            if hasattr(self.player2, 'strategy_type') and game % 30 == 0:   # against diverse agent, testing equally against all strategies
                self.player2.strategy_type = (self.player2.strategy_type % 5) + 1

            state = State()
            self.env.state = state
            player = self.player1
            while not self.env.is_end_of_game(state):
                action = player.get_action(state = state, train = False)
                state, _ = self.env.move_action(action = action)
                self.env.switch_players()
                self.env.roll_dice()
                player = self.switch_players(player)
                
            if self.env.end_of_game() == 1: white_win += 1
            elif self.env.end_of_game() == -1: black_win += 1
        print('finished testing:', black_win / games_num * 100,'%')
        return black_win, white_win

    def switch_players(self, player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1

# tester = Tester(env = env, player1 = player1, player2 = player2)
# games_num = 500
# black_win, white_win = tester.test(games_num)
# print('Black:', black_win, 'White:', white_win, '-->', black_win / games_num * 100,'%')