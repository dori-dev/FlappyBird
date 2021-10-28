"""constant variable in the game
"""

from os.path import join
import pygame
from tools import Tools

pygame.init()
clock = pygame.time.Clock()


WINDOW_WIDTH, WINDOW_HEIGHT = 420, 768
FLOOR_HEIGHT = 145
BEST_SCORE = 0
PIPE_GAP = 200
MAINMENU_ACTIVE = True
GAME_TICK = 30

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(pygame.image.load(join('data', 'icon.png')))

toolkit = Tools(WINDOW, join('data', 'sprites.png'))
world, bird_images, messages, buttons, numbers_img, scoreboard_img = toolkit.load_images()
