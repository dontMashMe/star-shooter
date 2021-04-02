import os

import pygame

# CONSTANTS
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pew pew")
WHITE = (255, 255, 255)
FPS = 60
VEL = 5  # velocity
BULLET_VEL = 10
background = pygame.image.load(os.path.join('Assets', 'space.png'))
bullet_asset = pygame.image.load(os.path.join('Assets', 'bullet.png'))


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
        WIN.blit(self.asset, (self.rectangle.x, self.rectangle.y))

    def rotate_bullet(self):
        self.asset = pygame.transform.rotate(self.asset, 90)


def handle_bullets(bullets: list):
    for bullet in bullets:
        bullet.rectangle.y -= BULLET_VEL
        if bullet.rectangle.y > HEIGHT:  # if the bullet reaches the end of the screen, remove it from the list
            bullets.remove(bullet)


def draw_window(spaceship_obj: SpaceShip, bullets: list):
    WIN.blit(background, (0, 0))
    spaceship_obj.draw_ship()
    for bullet in bullets:
        bullet.draw_bullet()
    pygame.display.update()


# driver code
def main():
    spaceship_object = SpaceShip(asset=pygame.image.load(os.path.join('Assets', 'spaceship_red.png')), ship_height=50,
                                 ship_width=40, starting_pos_x=WIDTH / 2 - 50,
                                 starting_pos_y=HEIGHT / 2 - 40, rotation=180)
    clock = pygame.time.Clock()
    run = True
    bullets = []
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:  # shooting
                if event.key == pygame.K_SPACE:
                    bullet_object = Bullet(bullet_asset, spaceship_object)
                    bullets.append(bullet_object)
                    print(bullets)

        keys_pressed = pygame.key.get_pressed()
        spaceship_object.handle_movement(keys_pressed)
        handle_bullets(bullets)
        draw_window(spaceship_object, bullets)

    pygame.quit()


if __name__ == "__main__":
    main()
