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

import os, pygame, projectiles
from pygame.locals import *

class PlayerSprite(pygame.sprite.Sprite):
    SPEED = 5
    FIRE_DELAY = 20

    def __init__(self, image, position, bounds, bullet_group):
        # Initialise the player
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.x_position, self.y_position = position
        self.k_left = self.k_right = self.k_fire = 0
        self.rect = self.image.get_rect()
        self.left_bound, self.right_bound, self.top_bound, self.bottom_bound = bounds
        self.fire_delay = 0
        self.bullet_group = bullet_group

    def update(self, events, collisions):
        if self in collisions:
            death = False
            for bullet in collisions[self]:
                if (bullet.origin != self):
                    bullet.kill()
                    death = True
            if (death == True):
                self.kill()


        # Update the player with current key information
        for event in events:
            if not hasattr(event, 'key'): continue # Now only interested in key presses
            down = event.type == KEYDOWN 
            if event.key == K_RIGHT: self.k_right = down
            elif event.key == K_LEFT: self.k_left = down
            elif event.key == K_SPACE: self.k_fire = down

        # Update the player, based on current settings of k_right and k_left
        self.x_position = self.x_position + self.SPEED*self.k_right - self.SPEED*self.k_left
        if self.x_position <= self.left_bound: 
            self.x_position = self.left_bound
        elif self.x_position >= self.right_bound:
            self.x_position = self.right_bound
        self.rect.center = (self.x_position, self.y_position)

        if (self.fire_delay > 0):
            self.fire_delay -= 1
        elif (self.fire_delay == 0 and self.k_fire != 0):
            self.fire()

    def fire(self):
        self.fire_delay = self.FIRE_DELAY
        bounds = (self.left_bound-100, self.right_bound+100, self.top_bound-100, self.bottom_bound+100)
        bullet = projectiles.Bullet(os.path.join("Resources", "Bullet.png"), (self.x_position, self.y_position), (0, -5), bounds, self)
        self.bullet_group.add(bullet)