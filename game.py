import pygame
import sys
from Graphics import *
from Environment import *
from State import *
from Human_Agent import *
from Random_Agent import *
from DQN_Agent import *
from Advanced_Random_Agent import *

def create_agent(type, id, env : Environment, graphics : Graphics):
    if type == 'Human Agent':
        return Human_Agent(id, env, graphics)
    elif type == 'Random Agent':
        return Random_Agent(id, env, graphics)
    elif type == 'Advanced Random Agent':
        return Advanced_Random_Agent(id, env, graphics)
    elif type == 'DQN Agent':
        return DQN_Agent(id, env = env, train = False)
    
def start_menu():
    screen = pygame.display.get_surface()
    options = ['Human Agent', 'Random Agent', 'Advanced Random Agent', 'DQN Agent']
    player1, player2 = 0, 0
    title_font = pygame.font.SysFont('timesnewroman', 60, True)
    label_font = pygame.font.SysFont('timesnewroman', 38, True)
    font = pygame.font.SysFont('timesnewroman', 30)

    option_rects1 = []
    option_rects2 = []

    while True:
        screen.fill((153, 76, 0))
        title_text = title_font.render('Backgammon', True, (20, 10, 0))
        screen.blit(title_text, (WIDTH//2 - title_text.get_width() // 2, 40))

        lbl1 = label_font.render('Player 1', True, (200, 200, 200))
        lbl2 = label_font.render('Player 2', True, (200, 200, 200))
        screen.blit(lbl1, (200, 140))
        screen.blit(lbl2, (800, 140))

        for i, option in enumerate(options):
            color1 = (255, 255, 0) if i == player1 else (200, 200, 200)
            txt1 = font.render(option, True, color1)
            rect1 = txt1.get_rect(topleft = (200, 240 + i * 60))
            option_rects1.append((rect1, i))
            screen.blit(txt1, rect1.topleft)

            color2 = (255, 255, 0) if i == player2 else (200, 200, 200)
            txt2 = font.render(option, True, color2)
            rect2 = txt2.get_rect(topleft = (800, 240 + i * 60))
            option_rects2.append((rect2, i))
            screen.blit(txt2, rect2.topleft)
        


        btn_w, btn_h = 200, 50
        start_rect = pygame.Rect(WIDTH // 2 - btn_w // 2, HEIGHT - 120, btn_w, btn_h)
        pygame.draw.rect(screen, (0, 0, 0), start_rect)
        start_txt = font.render('Start', True, (255, 255, 255))
        screen.blit(start_txt, (
            start_rect.x + btn_w // 2 - start_txt.get_width() // 2,
            start_rect.y + btn_h // 2 - start_txt.get_height() // 2
        ))

        pygame.display.flip()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, i in option_rects1:
                    if rect.collidepoint(event.pos):
                        player1 = i
                
                for rect, i in option_rects2:
                    if rect.collidepoint(event.pos):
                        player2 = i
                
                if start_rect.collidepoint(event.pos):
                    return options[player1], options[player2]

def end_menu(winner):
    screen = pygame.display.get_surface()
    title_font = pygame.font.SysFont('timesnewroman', 54, True)
    font = pygame.font.SysFont('timesnewroman', 30)

    options = ['Restart', 'Back To Menu', 'Quit']
    btns = []
    btn_w, btn_h, spacing = 250, 60, 40
    total_h = len(options) * btn_h + (len(options) - 1) * spacing
    start_y = HEIGHT // 2 - total_h // 2

    for i, label in enumerate(options):
        rect = pygame.Rect(WIDTH // 2 - btn_w // 2, start_y + i * (btn_h + spacing), btn_w, btn_h)
        btns.append((rect, label.lower().replace(' ', '_')))
    
    win_txt = title_font.render(f'Player {winner} Wins!', True, (255, 215, 0))

    while True:
        screen.fill((153, 76, 0))
        screen.blit(win_txt, (WIDTH//2 - win_txt.get_width() // 2, 100))

        for rect, action in btns:
            pygame.draw.rect(screen, (200, 200, 200), rect)
            txt = font.render(action.replace('_', ' ').title(), True, (0, 0, 0))
            screen.blit(txt, (
                rect.x + rect.width // 2 - txt.get_width() // 2,
                rect.y + rect.height // 2 - txt.get_height() // 2
            ))
        
        pygame.display.flip()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, action in btns:
                    if rect.collidepoint(event.pos):
                        return action
                    
def run_game(env : Environment, player1, player2, graphics : Graphics):
    player = player1

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        env.roll_dice()
        action = player.get_action(events = events, state = env.state)
        if action:
            env.move_action(action)
            player = player1 if player is player2 else player2
            env.switch_players()
        
        graphics(env.state)

        winner = env.end_of_game()
        if winner != 0:
            graphics.draw_winner(winner)
            return 1 if winner == -1 else 2

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

def main():
    pygame.init()
    graphics = Graphics()

    while True:
        type1, type2 = start_menu()
        while True:
            env = Environment(State())
            player1 = create_agent(type1, 1, env, graphics)
            player2 = create_agent(type2, 2, env, graphics)

            winner = run_game(env, player1, player2, graphics)
            
            choice = end_menu(winner)
            if choice == 'restart':
                continue
            elif choice == 'back_to_menu':
                break
            elif choice == 'quit':
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()