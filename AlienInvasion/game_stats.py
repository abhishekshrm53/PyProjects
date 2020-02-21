class GameStats:
    """Track stats"""
    def __init__(self, ai_game):
        """Initialize stats"""
        self.settings = ai_game.settings
        self.reset_stats()

        # Set state of game.
        self.game_active = True

    def reset_stats(self):
        """Stats that have to be reset during game"""
        self.ships_left = self.settings.ship_limit
