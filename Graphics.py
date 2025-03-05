import pygame
from Constants import *

class Graphics:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.head_surf = pygame.Surface((HEAD_WIDTH, HEAD_HEIGHT))
        self.main_surf = pygame.Surface((MAIN_WIDTH, MAIN_HEIGHT))
        pygame.display.set_caption('Backgammon')
        self.load_img()
    
    def __call__(self, state):
        self.draw(state)
        
    def load_img(self):
        self.title_img = pygame.image.load('images/title.png') # 1200 * 80
        self.board_img = pygame.image.load('images/board.png') # 1200 * 680
        self.red_triangle_img = pygame.image.load('images/triangle_red.png') # 80 * 280
        self.black_triangle_img = pygame.image.load('images/triangle_black.png') # 80 * 280
        self.white_checker_img = pygame.image.load('images/checker_white.png') # 56 * 56
        self.black_checker_img = pygame.image.load('images/checker_black.png') # 56 * 56
        self.dice1_img = pygame.image.load('images/dice1.png')
        self.dice2_img = pygame.image.load('images/dice2.png')
        self.dice3_img = pygame.image.load('images/dice3.png') # 50 * 50
        self.dice4_img = pygame.image.load('images/dice4.png')
        self.dice5_img = pygame.image.load('images/dice5.png')
        self.dice6_img = pygame.image.load('images/dice6.png')

    def draw(self, state):
        self.head_surf.blit(self.title_img, (0, 0))
        self.main_surf.blit(self.board_img, (0, 0))

        self.draw_title()
        self.draw_turn_info(state.player)
        self.draw_bottom_triangles()
        self.draw_top_triangles()
        self.draw_all_checkers(state)
        self.draw_dice(state.dice)

        self.screen.blit(self.head_surf, (0, 0))
        self.screen.blit(self.main_surf, (0, 80))
        pygame.display.flip()
    
    def draw_title(self):
        font = pygame.font.SysFont('timesnewroman', 54, True)
        text = font.render('Backgammon', True, (20, 10, 0))
        self.head_surf.blit(text, (HEAD_WIDTH / 2 - 150, 5))

    def draw_turn_info(self, player):
        font = pygame.font.SysFont('timesnewroman', 30, True)
        text = font.render('Turn:', True, (20, 10, 0))
        self.head_surf.blit(text, (50, 20))

        if player == -1:
            img = self.black_checker_img
        else:
            img = self.white_checker_img
        
        self.head_surf.blit(img, (125, 12))

    def draw_bottom_triangles(self):
        x, y = LEFT_SIDE_PADDING, TOP_PADDING + TRIANGLE_HEIGHT + TRIANGLES_PADDING
        for i in range(12):
            if i == 6:
                x += MIDDLE_WIDTH
            if i % 2 == 0:
                self.main_surf.blit(self.black_triangle_img, (x, y))
            else:
                self.main_surf.blit(self.red_triangle_img, (x, y))
            x += TRIANGLE_WIDTH

    def draw_top_triangles(self):
        x, y = LEFT_SIDE_PADDING, TOP_PADDING
        for i in range(12):
            if i == 6:
                x += MIDDLE_WIDTH
            if i % 2 == 0:
                self.main_surf.blit(pygame.transform.rotate(self.red_triangle_img, 180), (x, y))
            else:
                self.main_surf.blit(pygame.transform.rotate(self.black_triangle_img, 180), (x, y))
            x += TRIANGLE_WIDTH
    
    def draw_all_checkers(self, state):
        board = state.board
        for i in range(TRIANGLES_AMOUNT):
            if board[i] < 0:
                self.draw_triangle_checkers(i, board[i], self.black_checker_img)
            elif board[i] > 0:
                self.draw_triangle_checkers(i, board[i], self.white_checker_img)
        self.draw_checkers_eaten(state.checkers_eaten)
        self.draw_checkers_out(state.checkers_out)

    def draw_triangle_checkers(self, triangle_num, checkers_amount, img):
        checkers_amount = abs(checkers_amount)

        if triangle_num < 6:
            x = LEFT_SIDE_PADDING + TRIANGLE_WIDTH * (11 - triangle_num) + MIDDLE_WIDTH + ((TRIANGLE_WIDTH - CHECKER_WIDTH) / 2)
            y = TOP_PADDING + TRIANGLE_HEIGHT + TRIANGLES_PADDING + TRIANGLE_HEIGHT - CHECKER_HEIGHT
            for i in range(checkers_amount):
                self.main_surf.blit(img, (x, y))
                y -= CHECKER_HEIGHT / 1.6

        elif triangle_num < 12:
            x = LEFT_SIDE_PADDING + TRIANGLE_WIDTH * (11 - triangle_num) + ((TRIANGLE_WIDTH - CHECKER_WIDTH) / 2)
            y = TOP_PADDING + TRIANGLE_HEIGHT + TRIANGLES_PADDING + TRIANGLE_HEIGHT - CHECKER_HEIGHT
            for i in range(checkers_amount):
                self.main_surf.blit(img, (x, y))
                y -= CHECKER_HEIGHT / 1.6
        
        elif triangle_num < 18:
            x = LEFT_SIDE_PADDING + TRIANGLE_WIDTH * (triangle_num - 12) + ((TRIANGLE_WIDTH -  CHECKER_WIDTH) / 2)
            y = TOP_PADDING
            for i in range(checkers_amount):
                self.main_surf.blit(img, (x, y))
                y += CHECKER_HEIGHT / 1.6
        
        else:
            x = LEFT_SIDE_PADDING + TRIANGLE_WIDTH  * (triangle_num - 12) + MIDDLE_WIDTH + ((TRIANGLE_WIDTH - CHECKER_WIDTH) / 2)
            y= TOP_PADDING
            for i in range(checkers_amount):
                self.main_surf.blit(img, (x, y))
                y += CHECKER_HEIGHT / 1.6
        
    def draw_checkers_eaten(self, checkers_eaten):
        white_checkers_eaten, black_checkers_eaten = checkers_eaten
        x = LEFT_SIDE_PADDING + TRIANGLE_WIDTH * 6 + ((MIDDLE_WIDTH - CHECKER_WIDTH) / 2)
        y_white, y_black = TOP_PADDING + TRIANGLE_HEIGHT - CHECKER_HEIGHT - DICE_HEIGHT, TOP_PADDING + TRIANGLE_HEIGHT + TRIANGLES_PADDING + DICE_HEIGHT

        for i in range(white_checkers_eaten):
            self.main_surf.blit(self.white_checker_img, (x, y_white))
            y_white -= CHECKER_HEIGHT / 1.6
        
        for i in range(black_checkers_eaten):
            self.main_surf.blit(self.black_checker_img, (x, y_black))
            y_black += CHECKER_HEIGHT / 1.6
    
    def draw_checkers_out(self, checkers_out):
        white_checkers_out, black_checkers_out = checkers_out
        x = LEFT_SIDE_PADDING + 12 * TRIANGLE_WIDTH + MIDDLE_WIDTH + BOARD_RIGHT_SIDE_PADDING + ((CHECKERS_BOX_WIDTH - CHECKER_WIDTH) / 2)
        y_white, y_black = TOP_PADDING, TOP_PADDING + 2 * CHECKER_BOX_HEIGHT + CHECKERS_BOXES_PADDING - CHECKER_HEIGHT

        for i in range(white_checkers_out):
            self.main_surf.blit(self.white_checker_img, (x, y_white))
            y_white += CHECKER_HEIGHT / 3.3
        
        for i in range(black_checkers_out):
            self.main_surf.blit(self.black_checker_img, (x, y_black))
            y_black -= CHECKER_HEIGHT / 3.3

    def draw_dice(self, dice):
        dice1, dice2 = dice
        x = LEFT_SIDE_PADDING + TRIANGLE_WIDTH * 6 + ((MIDDLE_WIDTH - DICE_WIDTH) / 2)
        y_dice1, y_dice2 = TOP_PADDING + TRIANGLE_HEIGHT - DICE_HEIGHT / 2, TOP_PADDING + TRIANGLE_HEIGHT + TRIANGLES_PADDING - DICE_HEIGHT / 2
        self.main_surf.blit(self.get_dice_img(dice1), (x, y_dice1))
        self.main_surf.blit(self.get_dice_img(dice2), (x, y_dice2))
    
    def get_dice_img(self, dice):
        match dice:
            case 1:
                return self.dice1_img
            case 2:
                return self.dice2_img
            case 3:
                return self.dice3_img
            case 4:
                return self.dice4_img
            case 5:
                return self.dice5_img
            case 6:
                return self.dice6_img
    
    def get_area_num(self, pos):
        for i in range(AREAS_AMOUNT):
            if self.area_clicked(i, pos):
                return i
        return None

    def area_xy_minmax(self, area_num):
        if area_num is None:
            return None

        if area_num < 6:
            x_min = LEFT_SIDE_PADDING + TRIANGLE_WIDTH * (11 - area_num) + MIDDLE_WIDTH
            x_max = x_min + TRIANGLE_WIDTH
            y_min = HEAD_HEIGHT + TOP_PADDING + TRIANGLE_HEIGHT + TRIANGLES_PADDING
            y_max = y_min + TRIANGLE_HEIGHT
        elif area_num < 12:
            x_min = LEFT_SIDE_PADDING + TRIANGLE_WIDTH * (11 - area_num)
            x_max = x_min + TRIANGLE_WIDTH
            y_min = HEAD_HEIGHT + TOP_PADDING + TRIANGLE_HEIGHT + TRIANGLES_PADDING
            y_max = y_min + TRIANGLE_HEIGHT
        elif area_num < 18:
            x_min = LEFT_SIDE_PADDING + TRIANGLE_WIDTH * (area_num - 12)
            x_max = x_min + TRIANGLE_WIDTH
            y_min = HEAD_HEIGHT + TOP_PADDING
            y_max = y_min + TRIANGLE_HEIGHT
        elif area_num < 24:
            x_min = LEFT_SIDE_PADDING + TRIANGLE_WIDTH * (area_num - 12) + MIDDLE_WIDTH
            x_max = x_min + TRIANGLE_WIDTH
            y_min = HEAD_HEIGHT + TOP_PADDING
            y_max = y_min + TRIANGLE_HEIGHT
        elif area_num == 24:
            x_min = LEFT_SIDE_PADDING + 6 * TRIANGLE_WIDTH
            x_max = x_min + MIDDLE_WIDTH
            y_min = HEAD_HEIGHT + TOP_PADDING + TRIANGLE_HEIGHT + TRIANGLES_PADDING + DICE_HEIGHT / 2
            y_max = y_min + TRIANGLE_HEIGHT - DICE_HEIGHT / 2
        elif area_num == 25:
            x_min = LEFT_SIDE_PADDING + 6 * TRIANGLE_WIDTH
            x_max = x_min + MIDDLE_WIDTH
            y_min = HEAD_HEIGHT + TOP_PADDING
            y_max = y_min + TRIANGLE_HEIGHT - DICE_HEIGHT / 2
        elif area_num == 26:
            x_min = LEFT_SIDE_PADDING + 12 * TRIANGLE_WIDTH + MIDDLE_WIDTH + BOARD_RIGHT_SIDE_PADDING
            x_max = x_min + CHECKERS_BOX_WIDTH
            y_min = HEAD_HEIGHT + TOP_PADDING + CHECKER_BOX_HEIGHT + CHECKERS_BOXES_PADDING
            y_max = y_min + CHECKER_BOX_HEIGHT
        else:
            x_min = LEFT_SIDE_PADDING + 12 * TRIANGLE_WIDTH + MIDDLE_WIDTH + BOARD_RIGHT_SIDE_PADDING
            x_max = x_min + CHECKERS_BOX_WIDTH
            y_min = HEAD_HEIGHT + TOP_PADDING
            y_max = y_min + CHECKER_BOX_HEIGHT
        
        return x_min, x_max, y_min, y_max

    def area_clicked(self, area_num, pos):
        x, y = pos
        if (self.area_xy_minmax(area_num) is None):
            return False
        x_min, x_max, y_min, y_max = self.area_xy_minmax(area_num)
        return x_min <= x <= x_max and y_min <= y <= y_max

    def highlight_area(self, area_num):
        if (self.area_xy_minmax(area_num) is None):
            return
        
        x_min, x_max, y_min, y_max = self.area_xy_minmax(area_num)

        if area_num < 24:
            if area_num < 12:
                vertices = ((x_min, y_max), (x_max, y_max), (x_max - TRIANGLE_WIDTH / 2, y_min))
            elif area_num < 24:
                vertices = ((x_min, y_min), (x_max, y_min), (x_max - TRIANGLE_WIDTH / 2, y_max))
        else:
            vertices = ((x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max))
        
        pygame.draw.polygon(self.screen, 'BLACK', vertices)
        pygame.display.flip()
        pygame.time.delay(250)
        
    def draw_winner(self, winner):
        font = pygame.font.SysFont('timesnewroman', 56, True)

        if winner == -1:
            self.screen.blit(self.black_checker_img, (370, 395))
            self.screen.blit(self.black_checker_img, (930, 395))
        else:
            self.screen.blit(self.white_checker_img, (370, 395))
            self.screen.blit(self.white_checker_img, (930, 395))

        i = 0
        while i < 40:
            if i % 2 == 0:
                text = font.render('Winner:', True, (255, 0, 0))
            else:
                text = font.render('Winner:', True, (0, 0, 0))
                
            self.screen.blit(text, (170, 390))
            self.screen.blit(text, (730, 390))
            i += 1
            pygame.display.flip()
            pygame.time.delay(100)

    def draw_no_moves(self):
        font = pygame.font.SysFont('timesnewroman', 40, True)
        text = font.render('No moves available!', True, (0, 0, 0))
        self.screen.blit(text, (110, 390))
        self.screen.blit(text, (670, 390))
        pygame.display.flip()
        pygame.time.delay(1500)

    