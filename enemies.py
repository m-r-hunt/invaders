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

import os, random, pygame, projectiles, score_counter

class EnemySprite(pygame.sprite.Sprite):
    # Class for one enemy invader.
    def __init__(self, image, position, bullet_group):
        # image: relative path to an image pygame can load
        # position: (x, y) coordinates on screen
        # bullet_group: pygame.sprite.Group to put fired bullets in

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.bullet_group = bullet_group

    def update(self, dv, score, collisions):
        # Update this enemy. Should be called once per frame.
        # dv: (x, y) vector for movement this frame
        # score: a Score to increment on death
        # collisions: a dictionary of collisions, possibly containing this object
        # Handle any collisions given
        if self in collisions:
            death = False
            for bullet in collisions[self]:
                if (bullet.origin != self):
                    bullet.kill()
                    death = True
            if (death == True):
                score.increment()
                self.kill()
        # Update position
        self.position = (self.position[0] + dv[0], self.position[1] + dv[1])
        self.rect.center = self.position

    def y(self):
        # Return height (y coordinate).
        return self.position[1]

    def fire(self):
        # (Possibly) fire a bullet down.
        if (random.randrange(100) < 2):
            bounds = (0-100, 800+100, 0-100, 600+100)
            bullet = projectiles.Bullet(os.path.join("Resources", "Enemy Bullet.png"), self.position, (0, 5), bounds, self)
            self.bullet_group.add(bullet)



class EnemyColumn(pygame.sprite.Group):
    # Class for one column in a formation of enemies.
    # Exists so we can easily fire only the lowest enemy in each column
    # Remembers its own x coordinate, everything else happens inside the actual enemies
    def __init__(self, x_position):
        # x_position: integer x coordinate
        pygame.sprite.Group.__init__(self)
        self.x_position = x_position


    def update(self, dv, score, collisions):
        # Update this column. Should be called once per frame.
        # dv: (x, y) vector for movement this frame
        # score: a Score to pass to contained EnemySprites
        # collisions: a dictionary of collisions to pass to contained EnemySprites
        # Return (x, y), x of this column and y of lowest contained Sprite.
        self.x_position += dv[0]
        # Update contained sprites
        for i in self.sprites():
            i.update(dv, score, collisions)
        # Compute biggest y, ask that EnemySprite to fire.
        max_y = 0
        if (len(self) != 0):
            for i in self.sprites():
                if (i.y() > max_y):
                    max_y = i.y()
                    bottom_enemy = i
            bottom_enemy.fire()
        return self.x_position, max_y


class EnemyFormation(pygame.sprite.Group):
    # Class for a whole formation of enemies.
    # Contains both EnemyColumns and EnemySprites

    # Magic numbers: Base speed stepped horizontally or vertically each frame.
    H_STEP = 2
    V_STEP = 10

    def __init__(self, topleft, layout, bounds, bullet_group):
        pygame.sprite.Group.__init__(self)
        self.columns = []
        columns, rows = layout
        # Generate all the enemies and columns.
        for i in range(0, columns):
            column_x = topleft[0] + i*64
            enemy_column = EnemyColumn(topleft[0] + i*64)
            for j in range(0, rows):
                new_enemy = EnemySprite(os.path.join("resources", "Enemy.png"), (column_x, topleft[1] + j*64), bullet_group)
                enemy_column.add(new_enemy)
                self.add(new_enemy)
            self.columns.append(enemy_column)

        # Direction: +1 for right, -1 for left (i.e. +-ve x direction)
        self.current_direction = +1
        self.left_bound, self.right_bound, self.bottom_bound = bounds
        self.total = columns * rows

    def update(self, score, collisions):
        # Update this formation. Should be called once per frame.
        # score: a Score to pass to contained EnemyColumns
        # collisions: a dictionary of collisions to pass to contained EnemyColumns
        # Returns (bool, bool). First is True if this formation is still in a good state, False if it needs resetting.
        # Second is True if this is because it's now empty, False if it has reached the bottom of the screen.
        direction_change = too_low = False
        # Compute factor to move faster when we have fewer remaining members.
        scale = int(float(self.total)/float(len(self)))
        # Update columns
        for i in self.columns:
            x, y = i.update((scale*self.current_direction*self.H_STEP, 0), score, collisions)
            # Remove empty columns
            if (len(i.sprites()) == 0):
                self.columns.remove(i)
            # Notice if we've gone too low
            elif (y > self.bottom_bound):
                too_low = True
            # Remember to change direction when we reach screen edges
            elif (x < self.left_bound or x > self.right_bound):
                direction_change = True
        # Indicate we're empty
        if (len(self.columns) == 0):
            return False, True
        # Indicate we reached the bottom of the screen.
        elif too_low:
            return False, False
        # Drop down and change direction
        elif direction_change:
            self.current_direction *= -1
            for i in self.columns:
                i.update((scale*self.current_direction*self.H_STEP, self.V_STEP), score, [])
        # If we made it here, everything's fine.
        return True, True