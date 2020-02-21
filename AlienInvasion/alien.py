import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Class for alien to destroy"""

    def __init__(self, ai_game):
        """Initialize alien and its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load alien image and set alien rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Each alien starts at top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Alien position in floating point for precision
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien touches edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move aliens right"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
