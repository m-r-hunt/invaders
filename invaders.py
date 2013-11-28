# Invaders

# Copyright (C) 2013  Maximilian Hunt
# 
# This program is free software; you can redistribute it and/or modify

# it under the terms of the GNU General Public License as published by

# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.


# This program is distributed in the hope that it will be useful,

# but WITHOUT ANY WARRANTY; without even the implied warranty of

# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the

# GNU General Public License for more details.


# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,

# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os, sys, random, pygame, enemies, player, score_counter
from pygame.locals import *

class Invaders(object):
    def __init__(self, size):
        self.highscore = score_counter.HighScore()
        self.score = score_counter.ScoreCounter()
        try:
            with open("highscore.txt", "r") as hs_file:
                self.highscore.update(int(hs_file.readline()))
        except IOError:
            print "Couldn't open highscore.txt for reading"
        self.size = self.width, self.height = size
        self.black = 0,0,0
        self.wave = 1

    def invaders_quit(self):
        self.highscore.update(self.score.score)
        try:
            with open("highscore.txt", "w") as hs_file:
                hs_file.write("%d\n"%self.highscore.highscore)
        except IOError:
                print "Couldn't open highscore.txt for writing"
        sys.exit()

    def handle_global_events(self):
        events = pygame.event.get()
        for event in events:   
            if event.type == pygame.QUIT: 
                self.invaders_quit()
            if not hasattr(event, 'key'): continue # Now only interested in key presses
            if event.key == K_ESCAPE:
                self.invaders_quit()
        return events

    def death_screen(self):
        self.highscore.update(self.score.score)

        medtext = pygame.font.Font(pygame.font.get_default_font(), 80)
        notsobigtext = pygame.font.Font(pygame.font.get_default_font(), 150)

        ded = notsobigtext.render("YOU DIED", True, (255,255,255))
        topleft = ((self.width - ded.get_width())/2, (self.height - ded.get_height())/2)
        screen.blit(ded, topleft)
        score_text = medtext.render("Score = %d"%self.score.score, True, (255,255,255))
        topleft = ((self.width - score_text.get_width())/2, (self.height - ded.get_height())/2 + 150)
        screen.blit(score_text, topleft)
        pygame.display.flip()

        for i in range(0, 180):
            clock.tick(60)
            self.handle_global_events()

        self.score.__init__()
        self.wave = 1

    def wave_screen(self):
        medtext = pygame.font.Font(pygame.font.get_default_font(), 80)
        notsobigtext = pygame.font.Font(pygame.font.get_default_font(), 150)

        wave = notsobigtext.render("WAVE %d"%self.wave, True, (255,255,255))
        topleft = ((self.width - wave.get_width())/2, (self.height - wave.get_height())/2)
        screen.blit(wave, topleft)
        pygame.display.flip()

        for i in range(0, 60):
            clock.tick(60)
            self.handle_global_events()

    def draw_pause_screen(self, screen):
        bigtext = pygame.font.Font(pygame.font.get_default_font(), 180)
        overlay = pygame.Surface((800,600))
        overlay.fill((120,120,120))
        overlay.set_alpha(120)
        screen.blit(overlay, (0,0))
        pause = bigtext.render("PAUSED", True, (255,255,255))
        topleft = ((self.width - pause.get_width())/2, (self.height - pause.get_height())/2)
        screen.blit(pause, topleft)
        pygame.display.flip()

    def draw_scores(self, screen):
        text = pygame.font.Font(pygame.font.get_default_font(), 20)
        score_surf = text.render("Score = %d"%self.score.score, True, (255,255,255))
        hs_surf = text.render("Highscore = %d"%self.highscore.highscore, True, (255,255,255))
        screen.blit(score_surf, (0,0))
        screen.blit(hs_surf, (0,22))

    def reset_game(self, player_group, enemy_form, bullet_group):
        player_group.empty()
        bullet_group.empty()
        enemy_form.__init__((32,64), (8,4), (32, self.width-32, self.height - 75), bullet_group)
        my_player = player.PlayerSprite(os.path.join("resources", "Player.png"), (self.width/2, self.height-25), (20, self.width-20, 0, self.height), bullet_group)
        player_group.add(my_player)

    def main_loop(self, screen, clock):
        player_group = pygame.sprite.Group()
        bullet_group = pygame.sprite.Group()
        enemy_form = enemies.EnemyFormation((32,64), (8,4), (32, self.width-32, self.height - 75), bullet_group)
        self.reset_game(player_group, enemy_form, bullet_group)

        # Loop forever
        while 1:
            # Tick the clock and handle quitting
            clock.tick(60)
            events = self.handle_global_events()

            # Pause on loss of focus
            if (not pygame.key.get_focused()):
                self.draw_pause_screen(screen)
                while(not pygame.key.get_focused()):
                    clock.tick(60)
                    self.handle_global_events()

            # Continue as normal when we have focus
            else:
                # Repaint the screen
                screen.fill(self.black)

                # Update the player, handle player death
                player_kills = pygame.sprite.groupcollide(player_group, bullet_group, False, False)
                player_group.update(events, player_kills)
                if (len(player_group) == 0):
                    self.reset_game(player_group, enemy_form, bullet_group)
                    self.death_screen()

                # Update the enemy formation, handle both total enemy death and other player loss conditions
                enemy_kills = pygame.sprite.groupcollide(enemy_form, bullet_group, False, False)
                reset, alive = enemy_form.update(self.score, enemy_kills) 
                if (reset != True):
                    self.reset_game(player_group, enemy_form, bullet_group)
                    if (alive != True):
                        self.death_screen()
                    else:
                        self.wave += 1
                        self.wave_screen()

                # Update bullets
                bullet_group.update()

                # Draw everything
                bullet_group.draw(screen)
                enemy_form.draw(screen)
                player_group.draw(screen)
                self.draw_scores(screen)

                # Push the drawn frame
                pygame.display.flip()

# Begin actual code
pygame.init()
random.seed(0)
# Initialise screen and clock
size = (800, 600)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
game = Invaders(size)
game.main_loop(screen, clock)