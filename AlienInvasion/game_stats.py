class GameStats:
    """Track stats"""
    def __init__(self, ai_game):
        """Initialize stats"""
        self.settings = ai_game.settings
        self.reset_stats()

        # Set state of game.
        self.game_active = False

        self.high_score = 0

    def reset_stats(self):
        """Stats that have to be reset during game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
