# johanc
class Settings:
    """Stores settings for alien invasion"""

    def __init__(self):
        """Initial state of the game"""
        # screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)  # Background color

        # Ship settings
        self.ship_speed_multiplier = 2
        self.ship_limit = 4
        # Lasers
        self.laser_speed_multiplier = 3.1415
        self.laser_width = 3.14159
        self.laser_height = 15
        self.laser_color = 250, 250, 250
        self.lasers_allowed = 10
        # Enemies
        self.enemy_speed_multiplier = 16
        self.drop_speed = 20
        self.enemy_points = 50
        self.score_multiplier = 1.5
        # Game speed-up
        self.speedup_factor = 1.25
        # Positive is to the right negative is to the left
        self.fleet_direction = 1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Factors that change throughout the game"""
        self.ship_speed_multiplier = 1.25
        self.laser_speed_multiplier = 1.28
        self.enemy_speed_multiplier = 1
        self.fleet_direction = 1

    def increase_speed(self):
        """Gotta go fast"""
        self.ship_speed_multiplier *= self.speedup_factor
        self.enemy_speed_multiplier *= self.speedup_factor
        self.laser_speed_multiplier *= self.speedup_factor
        self.enemy_points = int(self.enemy_points * self.score_multiplier)
        print(self.enemy_points)
