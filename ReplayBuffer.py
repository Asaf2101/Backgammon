from collections import deque
import random
import torch
import numpy as np
from State import State

class ReplayBuffer:
    def __init__(self, capacity = 10000):
        self.buffer = deque(maxlen = capacity)

    def push(self, state : State, action, reward, next_state : State, done):
        # normalizing action pushed here, state already normalized
        self.buffer.append((state.to_tensor(), torch.from_numpy(np.array(action)) / 10, torch.tensor(reward), next_state.to_tensor(), torch.tensor(done)))

    def push_tensors(self, state_tensor, action_tensor, reward_tensor, next_state_tensor, done):
        self.buffer.append((state_tensor, action_tensor, reward_tensor, next_state_tensor, done))
    
    def sample(self, batch_size):
        if batch_size > self.__len__():
            batch_size = self.__len__()
        state_tensors, action_tensors, reward_tensors, next_state_tensors, dones = zip(*random.sample(self.buffer, batch_size))
        states = torch.vstack(state_tensors).to(torch.float32)
        #actions = torch.vstack(action_tensors)           # turns to [60, 2] instead of [30, 4]
        actions = torch.vstack(action_tensors).view(batch_size, -1).to(torch.float32)
        rewards = torch.vstack(reward_tensors).to(torch.float32)
        next_states = torch.vstack(next_state_tensors).to(torch.float32)
        done_tensor = torch.tensor(dones).long().reshape(-1,1).to(torch.float32)
        return states, actions, rewards, next_states, done_tensor
    
    def __len__(self):
        return len(self.buffer)