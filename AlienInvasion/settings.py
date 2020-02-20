class Settings:
    """A class to store game settings."""

    def __init__(self):
        """Initial settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.ship_speed = 1.5