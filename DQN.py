import math
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
from Constants import *

MSELoss = nn.MSELoss()

class DQN(nn.Module):
    def __init__(self):
        super().__init__()
        self.device = torch.device('cpu')
        self.linear1 = nn.Linear(input_size, layer1)
        self.linear2 = nn.Linear(layer1, layer2)
        # self.linear3 = nn.Linear(layer2, layer3)
        # self.output = nn.Linear(layer3, output_size)
        self.output = nn.Linear(layer2, output_size)
    
    def forward(self, x):
        x = self.linear1(x)
        x = F.leaky_relu(x)
        x = self.linear2(x)
        x = F.leaky_relu(x)
        # x = self.linear3(x)
        # x = F.leaky_relu(x)
        x = self.output(x)
        return x
    
    def load_params(self, path):
        self.load_state_dict(torch.load(path))
    
    def save_params(self, path):
        torch.save(self.state_dict(), path)
    
    def copy(self):
        new_DQN = DQN()
        new_DQN.load_state_dict(self.state_dict())
        return new_DQN

    def loss(self, Q_value, rewards, Q_next_values, dones):
        Q_new = rewards + gamma * Q_next_values * (1 - dones)
        return MSELoss(Q_value, Q_new)

    def __call__(self, states, actions):
        state_action = torch.cat((states, actions), dim = 1).to(torch.float32)
        return self.forward(state_action)