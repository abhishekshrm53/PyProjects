class Settings:
    """A class to store game settings."""

    def __init__(self):
        """Initial settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings.
        self.ship_speed = 3.0

        # Bullet settings.
        self.bullet_speed = 3.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 15

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 1
        # Fleet direction: 1 is right, -1 is left.
        self.fleet_direction = 1
