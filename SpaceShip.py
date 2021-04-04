import pygame
import Constants


class SpaceShip:
    def __init__(self, asset, ship_height: int, ship_width: int, starting_pos_x: float, starting_pos_y: float,
                 rotation: int):
        self.asset = asset
        self.ship_height = ship_height
        self.ship_width = ship_width
        self.resize_asset(ship_height, ship_width)
        self.rectangle = pygame.Rect(starting_pos_x, starting_pos_y, ship_width, ship_height)
        self.rotate_ship(rotation)
        self.health = 3

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


class Alien(SpaceShip):
    def __init__(self, asset, ship_height: int, ship_width: int, starting_pos_x: float, starting_pos_y: float,
                 rotation: int):
        super().__init__(asset, ship_height, ship_width, starting_pos_x, starting_pos_y, rotation)
        self.direction = 1  # indicates the direction of movement on the screen; 1 - left, -1 right, 0 stay still
        self.can_shoot = True

    def move(self):
        if self.direction == 1:
            self.rectangle.x -= Constants.ALIEN_VEL
        elif self.direction == -1:
            self.rectangle.x += Constants.ALIEN_VEL

    def explode(self):
        self.asset = Constants.explosion
        self.resize_asset(self.ship_height, self.ship_width)
        self.direction = 0
        self.draw_ship()
