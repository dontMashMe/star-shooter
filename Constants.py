import pygame
import os

pygame.init()

WIDTH, HEIGHT = 900, 500
VEL = 5  # velocity
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # window
BULLET_VEL = 10  # bullet velocity
pygame.display.set_caption("pew pew")
FPS = 60

# ASSETS
background = pygame.image.load(os.path.join('Assets', 'space.png')).convert()
bullet_asset = pygame.image.load(os.path.join('Assets', 'bullet.png'))

# SOUNDS
bullet_sound = pygame.mixer.Sound(os.path.join('Assets', 'laser-gun1.mp3'))
