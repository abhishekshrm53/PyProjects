import sys
import pygame
from AlienInvasion.settings import Settings
from AlienInvasion.ship import Ship


class AlienInvasion:
    """Main class of the game."""

    def __init__(self):
        """Initialize game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)

    def run_game(self):
        """Main game loop."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()

    def _update_screen(self):
        """Update Screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        # Make screen visible.
        pygame.display.flip()

    def _check_events(self):
        # Keyboard or Mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False


if __name__ == '__main__':
    # Make and run game.
    ai = AlienInvasion()
    ai.run_game()
