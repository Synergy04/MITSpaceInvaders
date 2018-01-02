# johanc

import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    # Initializes game and creates a screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Invaders")
    # Game statistic and scoreboard creation
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # Button creation
    play_button = Button(ai_settings, screen, "Play")
    # Ship creation
    ship = Ship(ai_settings, screen)
    # Make a group of lasers and enemies
    lasers = Group()
    enemies = Group()
    # Make enemies
    gf.create_fleet(ai_settings, screen, ship, enemies)
    # Main game loop
    while True:
        # Keyboard/Mouse event listener
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, enemies, lasers)
        if stats.game_active:
            ship.update()
            gf.update_lasers(ai_settings, screen, stats, sb, ship, lasers, enemies)
            gf.update_enemies(ai_settings, stats, screen, sb, ship, enemies, lasers)

        # Screen re-draw
        gf.update_screen(ai_settings, screen, stats, sb, ship, enemies, lasers, play_button)


run_game()
