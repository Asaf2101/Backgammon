import torch
from DQN import DQN
from DQN_Agent import DQN_Agent
from Random_Agent import Random_Agent
from Environment import Environment
from State import State
from ReplayBuffer import ReplayBuffer

epochs = 1000
C = 100
batch = 30
learning_rate = 0.1
path = "Data/test1.pth"

env = Environment(State())
player1 = DQN_Agent(1, env = env)
player2 = Random_Agent(2, env = env)
replay = ReplayBuffer()
Q = player1.DQN
Q_hat : DQN = Q.copy()
Q_hat.train = False
optim = torch.optim.Adam(Q.parameters(), lr = learning_rate)

for epoch in range(epochs):
    print('epoch =', epoch)
    step = 0
    state = State()
    env.state = state
    while not env.is_end_of_game(state):
        step += 1
        print('step', step, end="\r")
        
        og_state = state.copy()
        action = player1.get_action(state = state, epoch = epoch)
        after_state, reward1 = env.move_action(action = action)
        env.switch_players()   # switch players first
        env.roll_dice()

        done = env.is_end_of_game(after_state)
        if done:
            replay.push(og_state, action, reward1, after_state, done)
            break
               
        after_action = player2.get_action(state = after_state)
        next_state, reward2 = env.move_action(action = after_action)
        env.switch_players()   # switch players back
        env.roll_dice()
        
        reward = reward1 + reward2
        done = env.is_end_of_game(next_state)
        replay.push(og_state, action, reward, next_state, done)
        state = next_state
        
        if epoch < batch:
            continue

        states, actions, rewards, next_states, dones = replay.sample(batch)
        Q_values = Q(states, actions)
        next_actions = player1.get_actions(next_states, dones)
        with torch.no_grad():
            Q_hat_values = Q_hat(next_states, next_actions)
        loss = Q.loss(Q_values, rewards, Q_hat_values, dones)
        loss.backward()
        optim.step()
        optim.zero_grad()

    print('steps', step * 2)
    if epoch % C == 0:
        Q_hat.load_state_dict(Q.state_dict())
    
player1.save_params(path)