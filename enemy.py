import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):
    """Represents a single enemy"""

    def __init__(self, ai_settings, screen):
        """Creates enemy and sets it at starting position"""
        super(Enemy, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load enemy image
        self.image = pygame.image.load('res/enemy.bmp')
        self.rect = self.image.get_rect()

        # Origin at top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store position
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Returns true if at edge"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left < 0:
            return True

    def update(self):
        """Move"""
        self.x += self.ai_settings.enemy_speed_multiplier * self.ai_settings.fleet_direction
        self.rect.x = self.x
