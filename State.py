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

    def init(self, *args, **kwargs) -> None:
        pass

    def handle_input(self, *args, **kwargs) -> None:
        pass

    def handle_events(self, event) -> None:
        pass


class InGameState(State):

    def __init__(self, game_engine):
        self.score = 0
        self.game_engine = game_engine
        self.heart_containers = []
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
        self.spawn_aliens(4)
        # add three heart assets to a list
        self.heart_containers += 3 * [pygame.transform.scale(self.game_engine.assets.get("heart"), (36, 36))]

    def handle_input(self) -> None:
        keys_pressed = pygame.key.get_pressed()
        self.spaceship.handle_movement(keys_pressed)

    def draw(self) -> None:
        self.draw_background(self.game_engine)
        self.spaceship.draw_ship()
        score_text_surface = self.game_engine.font.render('Score: ' + str(self.score), False, (255, 255, 255))
        self.game_engine.WIN.blit(score_text_surface, (
            self.game_engine.constants.get("WIDTH") - score_text_surface.get_width() - 15,
            self.game_engine.constants.get("HEIGHT") - score_text_surface.get_height()))

        for i in range(len(self.heart_containers)):
            self.game_engine.WIN.blit(self.heart_containers[i],
                                      (0 + i * 30 + 15,
                                       self.game_engine.constants.get("HEIGHT") - self.heart_containers[
                                           i].get_height()))
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
            self.heart_containers[self.spaceship.health] = pygame.transform.scale(
                self.game_engine.assets.get("empty_heart"), (36, 36))
            if self.spaceship.health == 0:
                pygame.event.post(pygame.event.Event(self.game_engine.state_events.get(
                    "GAME_OVER")))  # this event is registered in the main loop of GameEngine
                return

    def update(self) -> None:
        self.handle_bullets()
        self.handle_alien_bullets()
        # handle_alien_bullets()
        for alien in self.aliens:
            if random.randrange(0, 100) < 1 and not alien.destroyed:
                bullet_object = Bullet.Bullet(self.game_engine.assets.get("bullet"), alien)
                bullet_object.shoot_sound()
                self.alien_bullets.append(bullet_object)
        if len(self.aliens) == 0:
            self.spawn_aliens(5)

    def handle_bullets(self):
        for bullet in self.bullets:
            bullet.rectangle.y -= self.game_engine.constants.get("BULLET_VEL")
            for alien in self.aliens:
                if alien.rectangle.colliderect(bullet.rectangle) and not alien.destroyed:
                    if not alien.destroyed:
                        self.score += 1 + self.score
                    alien.destroyed = True
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

    # to be called when all aliens are destroyed
    def spawn_aliens(self, number_of_aliens):
        last_pos = 0
        flip = random.randint(0, 1)
        for x in range(number_of_aliens):
            alien_object = SpaceShip.Alien(
                asset=self.game_engine.assets.get("alien"),
                ship_height=60,
                ship_width=50, starting_pos_x=self.game_engine.constants.get("WIDTH") / 1.5 - last_pos,
                starting_pos_y=self.game_engine.constants.get("HEIGHT") - 500, rotation=0)
            last_pos += 80
            if flip == 1:
                alien_object.direction = 1
            else:
                alien_object.direction = -1
            self.aliens.append(alien_object)


# TODO
class GameOver(State):
    print("game over")
