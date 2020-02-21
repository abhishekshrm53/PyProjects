import sys
import pygame
from AlienInvasion.settings import Settings
from AlienInvasion.ship import Ship
from AlienInvasion.bullet import Bullet
from AlienInvasion.alien import Alien


class AlienInvasion:
    """Main class of the game."""

    def __init__(self):
        """Initialize game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Make Alien fleet
        self._create_fleet()

    def run_game(self):
        """Main game loop."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

    def _update_screen(self):
        """Update Screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # Make screen visible.
        pygame.display.flip()

    def _check_events(self):
        # Keyboard or Mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Action for keypress"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Action for keyrelease"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create new fired bullet and add to group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        # Delete disappeared bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Check if bullet hit alien and remove both if hit
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """
        Check if fleet is at edge, and update
        position of all aliens.
        """
        self._check_fleet_edges()
        self.aliens.update()

    def _create_fleet(self):
        """Create fleet of aliens to destroy"""
        # Make alien and calculate aliens to fit in a row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        space_x = self.settings.screen_width - (2 * alien_width)
        num_aliens_x = space_x // (2 * alien_width)

        # Calculate number of rows for aliens
        ship_height = self.ship.rect.height
        space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        num_rows = space_y // (2 * alien_height)

        # Create first row
        for row_num in range(num_rows):
            for alien_num in range(num_aliens_x):
                # Create alien and place it on a row
                self._create_alien(alien_num, row_num)

    def _create_alien(self, alien_num, row_num):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_num
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_num
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Check if aliens are at edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()

    def _change_fleet_direction(self):
        """Drop fleet and invert direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


if __name__ == '__main__':
    # Make and run game.
    ai = AlienInvasion()
    ai.run_game()
