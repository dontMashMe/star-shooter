import os

import pygame

# CONSTANTS
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pew pew")
WHITE = (255, 255, 255)
FPS = 60
VEL = 5  # velocity


class SpaceShip:
    def __init__(self, asset, ship_height: int, ship_width: int, starting_pos_x: int, starting_pos_y: int,
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


def draw_window(spaceship_red: SpaceShip):
    WIN.fill(WHITE)
    spaceship_red.draw_ship()
    pygame.display.update()


# driver code
def main():
    spaceship_red = SpaceShip(pygame.image.load(os.path.join('Assets', 'spaceship_red.png')), 50, 40, 100, 300, 180)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]:  # LEFT
            spaceship_red.rectangle.x -= VEL
        if keys_pressed[pygame.K_d]:  # RIGHT
            spaceship_red.rectangle.x += VEL
        if keys_pressed[pygame.K_w]:
            spaceship_red.rectangle.y -= VEL
        if keys_pressed[pygame.K_s]:
            spaceship_red.rectangle.y += VEL
        draw_window(spaceship_red)

    pygame.quit()


if __name__ == "__main__":
    main()
