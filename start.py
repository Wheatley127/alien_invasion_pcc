import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button



class start:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Aliven Invasion")
        
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullet = pygame.sprite.Group()
        self.alien = pygame.sprite.Group()

        self._create_fleet()
       

        #make the play button
        self.play_button = Button(self, "Play")

       
        
        

    
    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullet()
                self._update_alien()
            
            self._update_screen()


            
    def _check_events(self):
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
        


    def _check_play_button(self, mouse_pos):
        """start a new game when a player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the settings
            self.settings.initialize_dynamic_settings()
            
            #reset stats
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
           

            self.alien.empty()
            self.bullet.empty()

            self._create_fleet()
            self.ship.center_ship()

            #hide the mouse 
            pygame.mouse.set_visible(False)
            
            
    def _check_keydown_events(self, event):

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        
        elif event.key == pygame.K_q:
            print("q key pressed") 
            sys.exit()
        
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
                
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

               

    def _fire_bullet(self):
        if len(self.bullet) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullet.add(new_bullet)
    
    def _update_bullet(self):
        self.bullet.update()
        
        # Get rid of bullets that have disappeared.
        for bullet in self.bullet.copy():
            if bullet.rect.bottom <= 0:
                self.bullet.remove(bullet)
            
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        """respond to a shot hit"""

        #check if a bullet hit an alien and remove them
        colisions = pygame.sprite.groupcollide(
            self.bullet, self.alien, True, True)

        if colisions:
            for alien in colisions.values():
                self.stats.score += self.settings.alien_points * len(alien)
                self.sb.prep_score()

        if not self.alien:
            #destroy existing bullets and create new fleetL
            self.bullet.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _update_alien(self):
        self._check_fleet_edges()
        self.alien.update()

        if pygame.sprite.spritecollideany(self.ship, self.alien):
            self._ship_hit()

        # look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.alien.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #treat this the same as if the ship dot hit
                self._ship_hit()
                break

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            
            self.alien.empty()
            self.bullet.empty()
            
            self._create_fleet()
            self.ship.center_ship()

            sleep(1.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """create the fleet of aliens"""
        #make an alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 + alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
        (3 * alien_height) - ship_height)

        number_rows = available_space_y // (2 * alien_height)

        #create the full fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.alien.add(alien)

    
    def _check_fleet_edges(self):
        """respond if an alien reached the edge"""
        for alien in self.alien.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """drop the fleet and change its diretion"""
        for alien in self.alien.sprites():
            alien.rect.y += self.settings.fleet_drop_Speed
        self.settings.fleet_direction *= -1


    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullet.sprites(): 
            bullet.draw_bullets()
        
        self.alien.draw(self.screen)
        
        #draw score info
        self.sb.show_score()
        
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()
        

if __name__ == '__main__':    
    ai = start()
    ai.run_game()