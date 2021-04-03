import pygame
import SpaceShip
import Constants as Constants


class Bullet:
    def __init__(self, asset, spaceship: SpaceShip):
        self.asset = asset
        self.resize_asset(50, 50)
        self.rotate_bullet()
        self.rectangle = pygame.Rect(spaceship.rectangle.x,
                                     spaceship.rectangle.y - 20, 10, 5)

    def resize_asset(self, width: int, height: int):
        self.asset = pygame.transform.scale(self.asset, (width, height))

    def draw_bullet(self):
        Constants.WIN.blit(self.asset, (self.rectangle.x, self.rectangle.y))

    def rotate_bullet(self):
        self.asset = pygame.transform.rotate(self.asset, 90)

    def shoot_sound(self):
        pygame.mixer.Sound.play(Constants.bullet_sound)
