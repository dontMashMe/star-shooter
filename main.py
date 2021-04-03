import pygame
import SpaceShip
import Constants
import Bullet
import random

SPACESHIP_HIT = pygame.USEREVENT + 1  # event for player getting hit
ALIEN_HIT = pygame.USEREVENT + 2  # event for player hitting alien
REMOVE_ALIEN = pygame.USEREVENT + 3

destroyed_aliens = []


# handling of bullets
def handle_bullets(bullets: list, aliens: list) -> None:
    for bullet in bullets:
        bullet.rectangle.y -= Constants.BULLET_VEL
        # if the bullet reaches the end of the screen, remove it from the list
        for alien in aliens:
            if alien.rectangle.colliderect(bullet.rectangle):
                alien.can_shoot = False
                bullets.remove(bullet)
                pygame.event.post(pygame.event.Event(ALIEN_HIT))
                destroyed_aliens.append(alien)
                pygame.time.set_timer(REMOVE_ALIEN, 500)
        if bullet.rectangle.y - bullet.rectangle.y < 0:
            bullets.remove(bullet)


def handle_alien_bullets(alien_bullets: list, spaceship: SpaceShip) -> None:
    for bullet in alien_bullets:
        bullet.rectangle.y += Constants.ALIEN_BULLET_VEL
        if spaceship.rectangle.colliderect(bullet.rectangle):  # check for alien bullet collision with player
            alien_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(SPACESHIP_HIT))
        if bullet.rectangle.y - bullet.rectangle.y > 0:
            alien_bullets.remove(bullet)


# drawing
def draw_window(spaceship_obj: SpaceShip.SpaceShip, bullets: list, bg_y: int, bg_y2: int, aliens: list,
                alien_bullets: list) -> None:
    Constants.WIN.blit(Constants.background, (0, bg_y))
    Constants.WIN.blit(Constants.background, (0, bg_y2))
    spaceship_obj.draw_ship()
    for bullet in bullets:
        bullet.draw_bullet()
    for alien_bullet in alien_bullets:
        alien_bullet.draw_bullet()

    for alien in aliens:
        alien.draw_ship()
        if not Constants.WIN.get_rect().contains(
                alien.rectangle):  # if the main window does not contain rectangle of alien, change the direction of
            # ALL aliens
            for alienb in aliens:
                alienb.direction *= -1
        alien.move()

    pygame.display.update()


# driver code
def main():
    spaceship_object = SpaceShip.SpaceShip(
        asset=Constants.red_ship,
        ship_height=50,
        ship_width=40, starting_pos_x=Constants.WIDTH / 2 - 50,
        starting_pos_y=Constants.HEIGHT / 2 - 40, rotation=180)

    alien_object = SpaceShip.Alien(
        asset=Constants.yellow_ship,
        ship_height=60,
        ship_width=50, starting_pos_x=Constants.WIDTH / 2 - 50,
        starting_pos_y=Constants.HEIGHT - 500, rotation=180)

    alien_object2 = SpaceShip.Alien(
        asset=Constants.yellow_ship,
        ship_height=60,
        ship_width=50, starting_pos_x=Constants.WIDTH / 2 + 50,
        starting_pos_y=Constants.HEIGHT - 500, rotation=180)

    bg_y = 0
    bg_y2 = Constants.background.get_height() * -1

    clock = pygame.time.Clock()
    run = True
    bullets = []
    aliens = [alien_object, alien_object2]
    alien_bullets = []
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
            if event.type == ALIEN_HIT:
                for alien in destroyed_aliens:
                    alien.explode()

            if event.type == REMOVE_ALIEN:
                for alien in destroyed_aliens:
                    destroyed_aliens.remove(alien)
                    aliens.remove(alien)

        # alien shooting
        for alien in aliens:
            if random.randrange(0, 100) < 1 and alien.can_shoot:
                bullet_object = Bullet.Bullet(Constants.bullet_asset, alien)
                bullet_object.shoot_sound()
                alien_bullets.append(bullet_object)

        keys_pressed = pygame.key.get_pressed()
        spaceship_object.handle_movement(keys_pressed)
        handle_bullets(bullets, aliens)
        handle_alien_bullets(alien_bullets, spaceship_object)
        draw_window(spaceship_object, bullets, bg_y, bg_y2, aliens, alien_bullets)

    pygame.quit()


if __name__ == "__main__":
    main()
