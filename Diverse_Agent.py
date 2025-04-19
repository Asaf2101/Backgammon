import pygame
import random
from Graphics import *
from Environment import *

class Diverse_Agent:
    def __init__(self, player, env : Environment, graphics : Graphics = None,
                 strategy_type = random.randint(1, 5)):
        self.player = player
        self.env = env
        self.graphics = graphics
        self.strategy_type = strategy_type
    
    def get_action(self, events = None, state = None, train = False):
        if self.graphics is not None:
            self.graphics(self.env.state)
        
        actions = self.env.get_all_actions(self.env.state)

        match self.strategy_type:
            case 1:      # true random
                return self.get_random_action(actions)
            case 2:      # prioritizes eating
                return self.get_eat_action(actions)
            case 3:      # prioritizes entering home then getting closer to home
                return self.get_enter_home_action(actions)
            case 4:      # prioritizes bearing off
                return self.get_bear_off_action(actions)
            case 5:      # prioritizes building anchors and avoiding single checkers
                return self.get_defensive_action(actions)
    

    # case 1

    def get_random_action(self, actions):
        return random.choice(actions)


    # case 2

    def get_eat_action(self, actions):
        filtered_actions = [a for a in actions if self.is_eat_action(a)]
        if filtered_actions: return random.choice(filtered_actions)
        else: return random.choice(actions)

    def is_eat_action(self, action):
        player = self.env.state.player
        board = self.env.state.board
        move1, move2 = action[0], action[1]

        if move1[1] != -1 and move1[1] != 26 and move1[1] != 27:
            if board[move1[1]] == -1 * player: return True
        if move2[1] != -1 and move2[1] != 26 and move2[1] != 27:
            if board[move2[1]] == -1 * player: return True
        
        return False


    # case 3

    def get_enter_home_action(self, actions):
        enter_home_actions = [a for a in actions if self.is_enter_home_action(a)]
        if enter_home_actions: return random.choice(enter_home_actions)

        towards_home_actions = [a for a in actions if not self.is_inside_home_action(a)]
        if towards_home_actions: return random.choice(towards_home_actions)

        return random.choice(actions)

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

    def is_inside_home_action(self, action):
        player = self.env.state.player
        move1, move2 = action[0], action[1]

        if player == -1:
            if 0 <= move1[0] <= 5: return True
            if 0 <= move2[0] <= 5: return True
        else:
            if 18 <= move1[0] <= 23: return True
            if 18 <= move2[0] <= 23: return True
        
        return False


    # case 4

    def get_bear_off_action(self, actions):
        both_bear_off = []
        one_bear_off = []

        for action in actions:
            result = self.is_bear_off_action(action)
            if result == 2:
                both_bear_off.append(action)
            if result == 1:
                one_bear_off.append(action)
        
        if both_bear_off: return random.choice(both_bear_off)
        elif one_bear_off: return random.choice(one_bear_off)
        else: return random.choice(actions)

    def is_bear_off_action(self, action):
        player = self.env.state.player
        move1, move2 = action[0], action[1]

        if player == -1:
            if move1[1] == 26 and move2[1] == 26: return 2
            if move1[1] == 26 or move2[1] == 26: return 1
        else:
            if move1[1] == 27 and move2[1] == 27: return 2
            if move1[1] == 27 or move2[1] == 27: return 1
        
        return 0


    # case 5

    def get_defensive_action(self, actions):
        best_action = None
        best_score = float('-inf')

        for action in actions:
            score = 0
            if self.creates_anchor(action): score += 1
            if self.creates_single_checkers(action): score -= 1

            if score > best_score:
                best_score = score
                best_action = action
        
        return best_action if best_action else random.choice(actions)

    def creates_anchor(self, action):
        player = self.env.state.player
        move1, move2 = action[0], action[1]
        og_state = self.env.state.copy()

        start_anchors = self.env.count_anchors(player)
        _ = self.env.move(move1)
        _ = self.env.move(move2)
        end_anchors = self.env.count_anchors(player)

        self.env.state = og_state
        
        return end_anchors > start_anchors

    def creates_single_checkers(self, action):
        player = self.env.state.player
        move1, move2 = action[0], action[1]
        og_state = self.env.state.copy()

        start_single_checkers = self.env.count_single_checkers(player)
        _ = self.env.move(move1)
        _ = self.env.move(move2)
        end_single_checkers = self.env.count_single_checkers(player)

        self.env.state = og_state

        return end_single_checkers > start_single_checkers

