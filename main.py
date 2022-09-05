import pygame, sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI

class Game:
    def __init__(self):
        # game attributes - user gui
        self.max_level = 0
        self.max_health = 100
        self.current_health = 100
        self.coins = 0

        # sound
        self.overworld_sound = pygame.mixer.Sound('./audio/overworld_OnAJourney.wav')
        self.overworld_sound.set_volume(0.08)

        self.level_sound = pygame.mixer.Sound('./audio/level_music.wav')
        self.level_sound.set_volume(0.08)

        # overworld creation
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.overworld_sound.play(loops=-1)

        # user interface
        self.ui = UI(screen)

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        self.overworld_sound.stop()
        self.level_sound.play(loops=-1)

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.level_sound.stop()
        self.overworld_sound.play(loops=-1)

    def change_coins(self, amount):
        self.coins += amount

    def change_health(self, amount_of_health):
        self.current_health += amount_of_health

    def check_game_over(self):
        if self.current_health <= 0:
            self.current_health = 100
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = 'overworld'
            self.level_sound.stop()
            self.overworld_sound.play(loops=-1)


    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.max_health, self.current_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    game.run()

    pygame.display.update()
    clock.tick(60)
