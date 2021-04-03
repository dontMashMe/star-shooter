import pygame
import os

pygame.init()

WIDTH, HEIGHT = 900, 500
VEL = 5  # velocity
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # window
BULLET_VEL = 10  # bullet velocity
ALIEN_VEL = 2
ALIEN_BULLET_VEL = 5
pygame.display.set_caption("pew pew")
FPS = 60

# ASSETS
background = pygame.image.load(os.path.join('Assets', 'space.png'))
bullet_asset = pygame.image.load(os.path.join('Assets', 'bullet.png'))
red_ship = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
yellow_ship = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
explosion = pygame.image.load(os.path.join('Assets', 'explosion.png'))

# SOUNDS
bullet_sound = pygame.mixer.Sound(os.path.join('Assets', 'laser-gun1.mp3'))
