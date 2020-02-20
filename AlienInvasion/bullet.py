import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class for bullets"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create bullet rect at (0, 0) and then set at correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Save bullet position.
        self.y = float(self.rect.y)

    def update(self):
        """Move bullet up"""
        # Update bullet position
        self.y -= self.settings.bullet_speed
        # Update rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullet on screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
