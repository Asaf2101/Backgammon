import torch

FPS = 60

WIDTH, HEIGHT = 1200, 760
HEAD_WIDTH, HEAD_HEIGHT = 1200, 80
MAIN_WIDTH, MAIN_HEIGHT = 1200, 680

AREAS_AMOUNT = 28
TRIANGLES_AMOUNT = 24

TRIANGLE_WIDTH, TRIANGLE_HEIGHT = 80, 280
CHECKER_WIDTH, CHECKER_HEIGHT = 56, 56
DICE_WIDTH, DICE_HEIGHT = 50, 50
CHECKERS_BOX_WIDTH, CHECKER_BOX_HEIGHT = 80, 290
MIDDLE_WIDTH = 80

LEFT_SIDE_PADDING, BOARD_RIGHT_SIDE_PADDING, TOP_PADDING = 30, 35, 30
TRIANGLES_PADDING = 60
CHECKERS_BOXES_PADDING = 40

input_size = 34
layer1 = 128
layer2 = 64
output_size = 1
gamma = 0.99

epsilon_start = 1
epsilon_final = 0.01
epsilon_decay = 50

epochs = 20000
C = 50
batch_size = 30
learning_rate = 0.001

if torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')
