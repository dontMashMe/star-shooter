import pygame
import Constants as Constants


class SpaceShip:
    def __init__(self, asset, ship_height: int, ship_width: int, starting_pos_x: float, starting_pos_y: float,
                 rotation: int):
        self.asset = asset
        self.ship_height = ship_height
        self.ship_width = ship_width
        self.resize_asset(ship_height, ship_width)
        self.rectangle = pygame.Rect(starting_pos_x, starting_pos_y, ship_width, ship_height)
        self.rotate_ship(rotation)

    def draw_ship(self):
        Constants.WIN.blit(self.asset, (self.rectangle.x, self.rectangle.y))

    def resize_asset(self, width: int, height: int):
        self.asset = pygame.transform.scale(self.asset, (width, height))

    def rotate_ship(self, angle: int):
        self.asset = pygame.transform.rotate(self.asset, angle)

    def handle_movement(self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.rectangle.x - Constants.VEL > 0:  # LEFT
            self.rectangle.x -= Constants.VEL

        if keys_pressed[pygame.K_d] and self.rectangle.x + Constants.VEL + self.ship_height < Constants.WIDTH:  # RIGHT
            self.rectangle.x += Constants.VEL

        if keys_pressed[pygame.K_w] and self.rectangle.y - Constants.VEL > 0:  # UP
            self.rectangle.y -= Constants.VEL

        if keys_pressed[pygame.K_s] and self.rectangle.y + Constants.VEL + self.ship_height < Constants.HEIGHT:  # DOWN
            self.rectangle.y += Constants.VEL
