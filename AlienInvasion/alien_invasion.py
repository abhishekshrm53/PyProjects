import sys
from time import sleep

import pygame

from AlienInvasion.settings import Settings
from AlienInvasion.ship import Ship
from AlienInvasion.bullet import Bullet
from AlienInvasion.alien import Alien
from AlienInvasion.game_stats import GameStats
from AlienInvasion.button import Button
from AlienInvasion.scoreboard import Scoreboard


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

        # Create an instance of stats.
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Make Alien fleet
        self._create_fleet()

        # Make play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Main game loop."""
        while True:
            self._check_events()

            if self.stats.game_active:
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
        self.scoreboard.show_score()

        # Draw play button to start game
        if not self.stats.game_active:
            self.play_button.draw_button()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

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
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.prep_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _update_aliens(self):
        """
        Check if fleet is at edge, and update
        position of all aliens.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Check if ship is hit.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check if aliens have reached bottom.
        self._check_aliens_bottom()

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
                break

    def _change_fleet_direction(self):
        """Drop fleet and invert direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Perform actions when ship is hit"""
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            # Delete remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and ship
            self._create_fleet()
            self.ship.centre_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if aliens have reached bottom"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Same as if ship was hit
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        """Start new game if play button is clicked."""
        button_click = self.play_button.rect.collidepoint(mouse_pos)
        if button_click and not self.stats.game_active:
            # Reset game
            self.settings.initialize_dynamic_settings()

            self.stats.reset_stats()
            self.stats.game_active = True

            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()

            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.centre_ship()

            pygame.mouse.set_visible(False)


if __name__ == '__main__':
    # Make and run game.
    ai = AlienInvasion()
    ai.run_game()
