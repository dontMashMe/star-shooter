import pygame
import os
import State


class GameEngine:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("pew pew")
        self.constants = {
            "WIDTH": 900,
            "HEIGHT": 500,
            "VEL": 5,
            "BULLET_VEL": 10,
            "ALIEN_BULLET_VEL": 5,
            "ALIEN_VEL": 2,
            "FPS": 60
        }
        self.assets = {
            "background": pygame.image.load(os.path.join('Assets', 'space.png')),
            "bullet": pygame.image.load(os.path.join('Assets', 'bullet.png')),
            "spaceship": pygame.image.load(os.path.join('Assets', 'spaceship_red.png')),
            "alien": pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png')),
            "explosion": pygame.image.load(os.path.join('Assets', 'explosion.png'))
        }
        self.sounds = {
            "bullets": pygame.mixer.Sound(os.path.join('Assets', 'laser-gun1.mp3'))
        }

        self.bg_y = 0
        self.bg_y2 = self.assets.get("background").get_height()
        self.WIN = pygame.display.set_mode((self.constants.get("WIDTH"), self.constants.get("HEIGHT")))
        self.clock = pygame.time.Clock()
        in_game_state = State.InGameState(self)
        state_game_over = State.GameOver()
        self.states = [in_game_state, state_game_over]

    def run(self, current_game_state: int):
        running = True
        self.states[current_game_state].init()
        while running:
            self.clock.tick(self.constants.get("FPS"))
            # scrolling background logic
            self.bg_y += 1.4
            self.bg_y2 += 1.4
            if self.bg_y > self.assets.get("background").get_height():
                self.bg_y = self.assets.get("background").get_height() * -1
            if self.bg_y2 > self.assets.get("background").get_height():
                self.bg_y2 = self.assets.get("background").get_height() * -1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.states[current_game_state].handle_events(event)
            self.states[current_game_state].draw()
            self.states[current_game_state].handle_input()
            self.states[current_game_state].update()
