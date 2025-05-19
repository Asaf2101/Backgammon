import torch
from DQN import DQN
from DQN_Agent import DQN_Agent
from Random_Agent import Random_Agent
from Environment import Environment
from State import State
from ReplayBuffer import ReplayBuffer
import wandb
import os
from Constants import *
from Tester import Tester
from Advanced_Random_Agent import Advanced_Random_Agent


def main():

    # Prepare data 
    env = Environment(State())
    player1 = DQN_Agent(1, env = env, train = True)
    # player2 = Random_Agent(2, env = env)
    player2 = Advanced_Random_Agent(2, env = env)
    buffer = ReplayBuffer()
    Q = player1.DQN
    Q_hat : DQN = Q.copy()
    Q_hat.train = False
    optim = torch.optim.Adam(Q.parameters(), lr = learning_rate)
    scheduler = torch.optim.lr_scheduler.StepLR(optim, step_size = 1500, gamma = 0.95)
    
    start_epoch = 0
    losses, wins_per_100, avg_checkers_diffs = [], [], []
    sum_diff, wins = 0, 0
    sum_diff10, wins10 = 0, 0

    # Prepare Tester
    tester = Tester(env, player1, player2)
    best_model_state_dict = player1.DQN.state_dict()
    best_win_precentage = 0

    # Load checkpoint if exists
    resume_wandb = False
    run_id = '-advTest13'
    checkpoint_path = f'Data/Player1/checkpoint{run_id}.pth'
    buffer_path = f'Data/Player1/buffer{run_id}.pth'
    path = f'Data/Player1/Model{run_id}.pth'
    if os.path.exists(checkpoint_path):
        resume_wandb = True
        checkpoint = torch.load(checkpoint_path)
        start_epoch = checkpoint['epoch'] + 1
        player1.DQN.load_state_dict(checkpoint['model_state_dict'])
        Q_hat.load_state_dict(checkpoint['model_state_dict'])
        best_model_state_dict = checkpoint['best_model_state_dict']
        optim.load_state_dict(checkpoint['optimizer_state_dict'])
        scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        buffer = torch.load(buffer_path)
        losses = checkpoint['loss']
        avg_checkers_diffs = checkpoint['avg_checkers_diff']
        wins_per_100 = checkpoint['wins_per_100']
        best_win_precentage = checkpoint['best_win_precentage']

    # Prepare wandb
    wandb.init(
        project = 'Backgammon',
        resume = resume_wandb,
        id = f'Backgammon {run_id}',
        config = {
            'name': f'Backgammon {run_id}',
            'checkpoint': checkpoint_path,
            'learning_rate': learning_rate,
            'scheduler': f'step size = {str(scheduler.step_size)}, gamma = {str(scheduler.gamma)}',
            'epochs': epochs,
            'start_epoch': start_epoch,
            'decay': epsilon_decay,
            'gamma': gamma,
            'batch_size': batch_size,
            'C': C,
            'model': str(player1.DQN),
            'device': str(device)
        }
    )
    

    # Training loop
    for epoch in range(start_epoch, epochs):
        state = State()
        env.state = state
        while not env.is_end_of_game(state):
            og_state = state.copy()
            action = player1.get_action(state = state, epoch = epoch)
            after_state, reward1 = env.move_action(action = action)
            env.switch_players()   # switch players first
            env.roll_dice()

            done = env.is_end_of_game(after_state)
            if done:
                buffer.push(og_state, action, reward1, after_state, done)
                break
                
            after_action = player2.get_action(state = after_state)
            next_state, reward2 = env.move_action(action = after_action)
            env.switch_players()   # switch players back
            env.roll_dice()
            
            reward = reward1 + reward2
            done = env.is_end_of_game(next_state)
            buffer.push(og_state, action, reward, next_state, done)
            state = next_state
            
            if len(buffer) < min_buffer or epoch < 301:
                continue
            
            states, actions, rewards, next_states, dones = buffer.sample(batch_size)
            Q_values = Q(states, actions)
            next_actions = player1.get_actions(next_states, dones)
            with torch.no_grad():
                Q_hat_values = Q_hat(next_states, next_actions)
            loss = Q.loss(Q_values, rewards, Q_hat_values, dones)
            loss.backward()
            optim.step()
            optim.zero_grad()

        if epoch % C == 0:
            Q_hat.load_state_dict(Q.state_dict())
        scheduler.step()
        
        # calc and print data
        checkers_diff = state.checkers_out[1] - state.checkers_out[0]
        sum_diff += checkers_diff
        sum_diff10 += checkers_diff
        if env.end_of_game() == -1:
            wins += 1
            wins10 += 1

        if epoch % 10 == 0 and epoch > 0 and epoch % 100 != 0:
            avg_checkers_diff = sum_diff10 / 10

            # only relate to loss when it got computed
            if 'loss' in locals():
                print(f'epoch: {epoch}, loss = {loss.item():.3f}, wins per 10: {wins10}, avg checkers diff: {avg_checkers_diff}')
            else:
                print(f'epoch: {epoch}, wins per 10: {wins10}, avg checkers diff: {avg_checkers_diff}')
            
            sum_diff10 = 0
            wins10 = 0

        if epoch % 100 == 0 and epoch > 0:
            avg_checkers_diff = sum_diff / 100
            
            # update data
            wins_per_100.append(wins)
            avg_checkers_diffs.append(avg_checkers_diff)
            
            log_data = {
                'Wins Per 100 Games': wins,
                'Average Checkers Diff Per 100 Games': avg_checkers_diff
            }

            # only relate to loss when it got computed
            if 'loss' in locals():
                log_data['Loss'] = loss
                losses.append(loss)
                print(f'epoch: {epoch}, loss = {loss.item():.3f}, wins per 100: {wins}, avg checkers diff: {avg_checkers_diff}')
            else:
                print(f'epoch: {epoch}, wins per 100: {wins}, avg checkers diff: {avg_checkers_diff}')

            wandb.log(log_data)

            sum_diff = 0
            wins = 0
            sum_diff10 = 0
            wins10 = 0
        
        # Test current model and save if has better win precentage
        if epoch % 200 == 0 and epoch > 0:
            player1.train = False
            player1.train_mode()
            win_precentage = tester.test(300)[0]
            if win_precentage > best_win_precentage:
                best_win_precentage = win_precentage
                best_model_state_dict = player1.DQN.state_dict()
            player1.train = True
            player1.train_mode()

        # save checkpoint
        if epoch % 1000 == 0 and epoch > 0:
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': player1.DQN.state_dict(),
                'best_model_state_dict': best_model_state_dict,
                'optimizer_state_dict': optim.state_dict(),
                'scheduler_state_dict' : scheduler.state_dict(),
                'loss': losses,
                'avg_checkers_diff': avg_checkers_diffs,
                'wins_per_100': wins_per_100,
                'best_win_precentage': best_win_precentage
            }
            torch.save(checkpoint, checkpoint_path)
            torch.save(buffer, buffer_path)
            print('saved checkpoint')
        

    player1.save_params(path)
    
    wandb.finish()

if __name__  == '__main__':
    main()