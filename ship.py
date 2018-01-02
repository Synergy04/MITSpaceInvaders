#johanc
import pygame
from pygame.sprite import Sprite
class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        super(Ship,self).__init__()
        '''Initializes the ship and sets its origin'''
        self.screen = screen
        self.ai_settings = ai_settings
        #load ship
        self.image = pygame.image.load('res/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        #ship at the bottom
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        #decimal value of ship's center
        self.center = float(self.rect.centerx)
        #Movement flag
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        '''Centers ship'''
        self.center = self.screen_rect.centerx

    def update(self):
        '''Update position based on flag'''
        if self.moving_right and self.rect.right < self.screen_rect.right: #Makes sure it doesn't go off screen
            self.center += self.ai_settings.ship_speed_multiplier
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_multiplier
        self.rect.centerx = self.center

    def blitme(self):
        '''Draw ship'''
        self.screen.blit(self.image,self.rect)