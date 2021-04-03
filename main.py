import pygame
import SpaceShip as SpaceShip
import Constants as Constants
import Bullet as Bullet


# handling of bullets
def handle_bullets(bullets: list):
    for bullet in bullets:
        bullet.rectangle.y -= Constants.BULLET_VEL
        if bullet.rectangle.y < 0:  # if the bullet reaches the end of the screen, remove it from the list
            bullets.remove(bullet)


# drawing
def draw_window(spaceship_obj: SpaceShip.SpaceShip, bullets: list, bg_y: int, bg_y2: int):
    Constants.WIN.blit(Constants.background, (0, bg_y))
    Constants.WIN.blit(Constants.background, (0, bg_y2))
    spaceship_obj.draw_ship()
    for bullet in bullets:
        bullet.draw_bullet()
    pygame.display.update()


# driver code
def main():
    spaceship_object = SpaceShip.SpaceShip(
        asset=pygame.image.load(Constants.os.path.join('Assets', 'spaceship_red.png')),
        ship_height=50,
        ship_width=40, starting_pos_x=Constants.WIDTH / 2 - 50,
        starting_pos_y=Constants.HEIGHT / 2 - 40, rotation=180)

    bg_y = 0
    bg_y2 = Constants.background.get_height() * -1

    clock = pygame.time.Clock()
    run = True
    bullets = []
    while run:
        clock.tick(Constants.FPS)

        # scrolling background logic
        bg_y += 1.4
        bg_y2 += 1.4
        if bg_y > Constants.background.get_height():
            bg_y = Constants.background.get_height() * -1

        if bg_y2 > Constants.background.get_height():
            bg_y2 = Constants.background.get_height() * -1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:  # shooting
                if event.key == pygame.K_SPACE:
                    bullet_object = Bullet.Bullet(Constants.bullet_asset, spaceship_object)
                    bullet_object.shoot_sound()
                    bullets.append(bullet_object)

        keys_pressed = pygame.key.get_pressed()
        spaceship_object.handle_movement(keys_pressed)
        handle_bullets(bullets)
        draw_window(spaceship_object, bullets, bg_y, bg_y2)

    pygame.quit()


if __name__ == "__main__":
    main()
