class Settings:

    def __init__(self):

       

    
        
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        
        #ship settings
        self.ship_limit = 3

        #bullet setting
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3
        
        #alieb settings
        self.fleet_drop_Speed = 3
        
        #how quickly the game speeds up
        self.speedup_scale = 1.1
        #how quickly the point valus increase
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.5
        
        self.fleet_direction = -1

        
        
        #scoring
        self.alien_points = 50 

    

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)




