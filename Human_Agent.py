import pygame
from Graphics import *
from Environment import *

class Human_Agent:
    def __init__(self, player, env : Environment, graphics : Graphics):
        self.player = player
        self.env = env
        self.graphics = graphics
        self.mode = 0
    
    def get_action(self, events, state = None):
        self.graphics(self.env.state)

        if self.env.state.blocked == 2:
            return ((-1, -1), (-1, -1))

        if self.mode == 0 and self.env.slow_get_all_actions() == [((-1, -1), (-1, -1))]:
            self.graphics.draw_no_moves()
            return ((-1, -1), (-1, -1))
        
        if self.mode == 2 and ((self.from_area1, self.to_area1), (-1, -1)) in self.possible_turn_actions:
            self.mode = 0
            self.env.state = self.state_copy
            self.graphics.draw_no_moves()
            return ((self.from_area1, self.to_area1), (-1, -1))

        pos = None
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
        
        if pos is None: return None
        area_clicked = self.graphics.get_area_num(pos)
        if area_clicked is None: return None
        self.graphics.highlight_area(area_clicked)

        if self.mode == 0:
            self.possible_turn_actions = self.env.slow_get_all_actions()
            self.from_area1 = area_clicked
            self.mode = 1
            self.state_copy = self.env.state.copy()
            return None
        elif self.mode == 1:
            self.to_area1 = area_clicked
            self.dice_needed1 = self.env.legal_move((self.from_area1, self.to_area1))
            if self.dice_needed1 == False: self.mode = 0
            else:
                self.mode = 2
                self.env.move((self.from_area1, self.to_area1))
            return None
        elif self.mode == 2:
            self.from_area2 = area_clicked
            self.mode = 3
            return None
        else:
            self.to_area2 = area_clicked
            self.dice_needed2 = self.env.legal_move((self.from_area2, self.to_area2))
            if self.dice_needed2 == False:
                self.mode = 2
                return None
            
            elif self.env.legal_action(self.dice_needed1, self.dice_needed2) == False:
                self.mode = 0
                self.env.state = self.state_copy
                return None
            
            else:
                self.mode = 0
                self.env.state = self.state_copy
                return((self.from_area1, self.to_area1), (self.from_area2, self.to_area2))

    