import pygame
from pygame.sprite import Sprite


class Laser(Sprite):
    '''Fires lasers'''

    def __init__(self, ai_settings, screen, ship):
        super(Laser, self).__init__()
        self.screen = screen

        # Create laser rect at origin then update position
        self.rect = pygame.Rect(0, 0, ai_settings.laser_width, ai_settings.laser_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Position as float
        self.y = float(self.rect.y)

        self.color = ai_settings.laser_color
        self.speed_multiplier = ai_settings.laser_speed_multiplier

    def update(self):
        '''Shot laser (updates position)'''
        self.y -= self.speed_multiplier
        self.rect.y = self.y

    def draw_laser(self):
        '''Draws laser'''
        pygame.draw.rect(self.screen, self.color, self.rect)
