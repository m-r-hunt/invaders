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

import pygame

class Bullet(pygame.sprite.Sprite):
    # Class for a bullet fired by anyone.

    def __init__(self, image, position, velocity, bounds, origin):
        # image: relative path to an image pygame can load
        # position: (x, y) coordinates on screen
        # velocity: (u, v) vector, remains the same forever
        # bounds: (a, b) Furthest left and right to go.
        # origin: starting position of this bullet
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.position = position
        self.velocity = velocity
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.left_bound, self.right_bound, self.top_bound, self.bottom_bound = bounds
        self.origin = origin

    def update(self):
        # Update this bullet. Should be called once per frame.
        # Keep flying in the same direction until we go out of bounds.
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        self.rect.center = self.position
        if (self.position[0] < self.left_bound or self.position[0] > self.right_bound or self.position[1] < self.top_bound or self.position[1] > self.bottom_bound):
            self.kill()