import pygame
from Graphics import *
from Environment import *
from State import *
from Human_Agent import *
from Random_Agent import *
from DQN_Agent import DQN_Agent

import timeit

pygame.init()

graphics = Graphics()
env = Environment(State())

player1 = Human_Agent(1, env, graphics)
# player2 = Human_Agent(2, env, graphics)
# player1 = Random_Agent(1, env, graphics)
# player2 = Random_Agent(2, env, graphics)
# player1 = DQN_Agent(1, env = env, train = False)
player2 = DQN_Agent(2, env = env, train = False)

player = player1
graphics(env.state)

def switch_players(player):
    if player == player1:
        return player2
    else:
        return player1

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False

    env.roll_dice()
    action = player.get_action(events = events, state = env.state)
    if action:
        env.move_action(action)
        player = switch_players(player)
        env.switch_players()

    graphics(env.state)

    if env.end_of_game() != 0:
        run = False
        graphics.draw_winner(env.end_of_game())

    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

pygame.quit()