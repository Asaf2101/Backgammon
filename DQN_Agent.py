import math
import random
import pygame
import numpy as np
from typing import Any
import torch
import torch.nn as nn
from DQN import DQN
from State import State
from Environment import Environment

epsilon_start = 1
epsilon_final = 0.01
epsiln_decay = 5000

gamma = 0.99 
MSELoss = nn.MSELoss()

class DQN_Agent:
    def __init__(self, player = 1, parameters_path = None, train = True, env : Environment = None):
        self.DQN = DQN()
        if parameters_path:
            self.DQN.load_params(parameters_path)
        self.train(train)
        # self.train = train
        self.player = player
        self.env = env
    
    def train(self, train):
        self.train = train
        if train:
            self.DQN.train()
        else:
            self.DQN.eval()
    
    def get_action(self, state : State, epoch = 0, events = None, train = False):
        # pygame.time.delay(1500)
        epsilon = self.epsilon_greedy(epoch)
        rnd = random.random()
        actions = self.env.get_all_actions(state)
        
        if self.train and train and rnd < epsilon:
            return random.choice(actions)

        state_tensor = state.to_tensor()
        actions_np = np.array(actions)
        actions_tensor = torch.from_numpy(actions_np).reshape(-1, 4).to(torch.float32)
        expand_state_tensor = state_tensor.unsqueeze(0).repeat((len(actions_tensor), 1)).to(torch.float32)
        # state_action = torch.cat((expand_state_tensor, actions_tensor), dim = 1)
        with torch.no_grad():
            Q_values = self.DQN(expand_state_tensor, actions_tensor)
        max_index = torch.argmax(Q_values)
        return actions[max_index]

    def get_actions(self, states, dones):
        actions = []
        for i, state in enumerate(states):
            if dones[i].item():
                actions.append(((-1, -1), (-1, -1)))
            else:
                actions.append(self.get_action(state = State.to_state(state, self.player), train = True))
        return torch.tensor(actions).view(-1, 4).to(torch.float32)

    def epsilon_greedy(self, epoch, start = epsilon_start, final = epsilon_final, decay = epsiln_decay):
        res = final + (start - final) * math.exp(-1 * epoch/decay)
        return res

    def save_params(self, path):
        self.DQN.save_params(path)
    
    def load_params(self, path):
        self.DQN.load_params(path)
    
    def __call__(self, events = None, state = None):
        return self.get_action(state)

