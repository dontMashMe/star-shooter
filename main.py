import os

import pygame

# CONSTANTS
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pew pew")
WHITE = (255, 255, 255)
FPS = 60
VEL = 5  # velocity
background = pygame.image.load(os.path.join('Assets', 'space.png'))


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
        WIN.blit(self.asset, (self.rectangle.x, self.rectangle.y))

    def resize_asset(self, width: int, height: int):
        self.asset = pygame.transform.scale(self.asset, (width, height))

    def rotate_ship(self, angle: int):
        self.asset = pygame.transform.rotate(self.asset, angle)

    def handle_movement(self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.rectangle.x - VEL > 0:  # LEFT
            self.rectangle.x -= VEL

        if keys_pressed[pygame.K_d] and self.rectangle.x + VEL + self.ship_height < WIDTH:  # RIGHT
            self.rectangle.x += VEL

        if keys_pressed[pygame.K_w] and self.rectangle.y - VEL > 0:  # UP
            self.rectangle.y -= VEL

        if keys_pressed[pygame.K_s] and self.rectangle.y + VEL + self.ship_height < HEIGHT:  # DOWN
            self.rectangle.y += VEL


def draw_window(spaceship_obj: SpaceShip):
    WIN.blit(background, (0, 0))
    spaceship_obj.draw_ship()
    pygame.display.update()


# driver code
def main():
    spaceship_object = SpaceShip(pygame.image.load(os.path.join('Assets', 'spaceship_red.png')), 50, 40, WIDTH / 2 - 50,
                                 HEIGHT / 2 - 40, 180)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        spaceship_object.handle_movement(keys_pressed)
        draw_window(spaceship_object)

    pygame.quit()


if __name__ == "__main__":
    main()
