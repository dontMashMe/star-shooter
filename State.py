# super class containing methods for displaying and drawing each state of finite state machine
import pygame
import SpaceShip
import Bullet
import random


class State:

    # handles drawing of background, this is the same for all states so we can define it here
    def draw_background(self, game_engine):
        game_engine.WIN.blit(game_engine.assets.get("background"), (0, game_engine.bg_y))
        game_engine.WIN.blit(game_engine.assets.get("background"), (0, game_engine.bg_y2))

    def draw(self, *args, **kwargs) -> None:
        pass

    # call in event loop
    def update(self, *args, **kwargs) -> None:
        pass

    def process_input(self, *args, **kwargs) -> None:
        pass

    def init(self, *args, **kwargs) -> None:
        pass

    def handle_input(self, *args, **kwargs) -> None:
        pass

    def handle_events(self, event) -> None:
        pass


class InGameState(State):

    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.aliens = []
        self.alien_bullets = []
        self.bullets = []
        self.destroyed_aliens = []
        self.SPACESHIP_HIT = pygame.USEREVENT + 1  # event for player getting hit
        self.ALIEN_HIT = pygame.USEREVENT + 2  # event for player hitting alien
        self.REMOVE_ALIEN = pygame.USEREVENT + 3  # event for timer that removes alien from list of aliens to render
        self.spaceship = SpaceShip.SpaceShip(
            asset=self.game_engine.assets.get("spaceship"),
            ship_height=50,
            ship_width=40, starting_pos_x=self.game_engine.constants.get("WIDTH") / 2 - 50,
            starting_pos_y=self.game_engine.constants.get("HEIGHT") / 2 - 40, rotation=180)

    def init(self) -> None:

        alien_object = SpaceShip.Alien(
            asset=self.game_engine.assets.get("alien"),
            ship_height=60,
            ship_width=50, starting_pos_x=self.game_engine.constants.get("WIDTH") / 2 - 50,
            starting_pos_y=self.game_engine.constants.get("HEIGHT") - 500, rotation=180)
        alien_object2 = SpaceShip.Alien(
            asset=self.game_engine.assets.get("alien"),
            ship_height=60,
            ship_width=50, starting_pos_x=self.game_engine.constants.get("WIDTH") / 2 + 50,
            starting_pos_y=self.game_engine.constants.get("HEIGHT") - 500, rotation=180)
        self.aliens.append(alien_object)
        self.aliens.append(alien_object2)

    def handle_input(self) -> None:
        keys_pressed = pygame.key.get_pressed()
        self.spaceship.handle_movement(keys_pressed)

    def draw(self) -> None:
        self.draw_background(self.game_engine)
        self.spaceship.draw_ship()
        for bullet in self.bullets:
            bullet.draw_bullet()
        for alien_bullet in self.alien_bullets:
            alien_bullet.draw_bullet()
        for alien in self.aliens:
            alien.draw_ship()
            if not self.game_engine.WIN.get_rect().contains(
                    alien.rectangle):  # if the main window does not contain rectangle of alien, change the direction of
                # ALL aliens
                for alienb in self.aliens:
                    alienb.direction *= -1
            alien.move()
        pygame.display.update()

    def handle_events(self, event) -> None:
        if event.type == pygame.KEYDOWN:  # shooting
            if event.key == pygame.K_SPACE:
                bullet_object = Bullet.Bullet(self.game_engine.assets.get("bullet"), self.spaceship)
                bullet_object.shoot_sound()
                self.bullets.append(bullet_object)

        if event.type == self.ALIEN_HIT:
            for alien in self.destroyed_aliens:
                alien.explode()
        if event.type == self.REMOVE_ALIEN:
            for alien in self.destroyed_aliens:
                if self.destroyed_aliens.__contains__(alien):
                    self.destroyed_aliens.remove(alien)
                if self.aliens.__contains__(alien):
                    self.aliens.remove(alien)
        if event.type == self.SPACESHIP_HIT:
            self.spaceship.health -= 1

    def update(self) -> None:
        self.handle_bullets()
        self.handle_alien_bullets()
        # handle_alien_bullets()
        for alien in self.aliens:
            if random.randrange(0, 100) < 1 and alien.can_shoot:
                bullet_object = Bullet.Bullet(self.game_engine.assets.get("bullet"), alien)
                bullet_object.shoot_sound()
                self.alien_bullets.append(bullet_object)

    def handle_bullets(self):
        for bullet in self.bullets:
            bullet.rectangle.y -= self.game_engine.constants.get("BULLET_VEL")
            for alien in self.aliens:
                if alien.rectangle.colliderect(bullet.rectangle):
                    alien.can_shoot = False
                    self.bullets.remove(bullet)
                    pygame.event.post(pygame.event.Event(self.ALIEN_HIT))
                    self.destroyed_aliens.append(alien)
                    pygame.time.set_timer(self.REMOVE_ALIEN, 500)
                if bullet.rectangle.y - bullet.rectangle.y < 0:
                    self.bullets.remove(bullet)

    def handle_alien_bullets(self):
        for bullet in self.alien_bullets:
            bullet.rectangle.y += self.game_engine.constants.get("ALIEN_BULLET_VEL")
            if self.spaceship.rectangle.colliderect(
                    bullet.rectangle):  # check for alien bullet collision with player
                self.alien_bullets.remove(bullet)
                pygame.event.post(pygame.event.Event(self.SPACESHIP_HIT))
            if bullet.rectangle.y - bullet.rectangle.y > 0:
                self.alien_bullets.remove(bullet)


# TODO
class GameOver(State):
    pass
