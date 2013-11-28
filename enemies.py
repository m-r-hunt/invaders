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
    def __init__(self, image, position, bullet_group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.bullet_group = bullet_group

    def update(self, dv, score, collisions):
        if self in collisions:
            death = False
            for bullet in collisions[self]:
                if (bullet.origin != self):
                    bullet.kill()
                    death = True
            if (death == True):
                score.increment()
                self.kill()
        self.position = (self.position[0] + dv[0], self.position[1] + dv[1])
        self.rect.center = self.position

    def height(self):
        return self.position[1]

    def fire(self):
        if (random.randrange(100) < 2):
            bounds = (0-100, 800+100, 0-100, 600+100)
            bullet = projectiles.Bullet(os.path.join("Resources", "Enemy Bullet.png"), self.position, (0, 5), bounds, self)
            self.bullet_group.add(bullet)



class EnemyColumn(pygame.sprite.Group):
    def __init__(self, x_position):
        pygame.sprite.Group.__init__(self)
        self.x_position = x_position


    def update(self, dv, score, collisions):
        self.x_position += dv[0]
        for i in self.sprites():
            i.update(dv, score, collisions)
        max_height = 0
        if (len(self) != 0):
            for i in self.sprites():
                if (i.height() > max_height):
                    max_height = i.height()
                    bottom_enemy = i
            bottom_enemy.fire()
        return self.x_position, max_height


class EnemyFormation(pygame.sprite.Group):
    H_STEP = 2
    V_STEP = 10

    def __init__(self, topleft, layout, bounds, bullet_group):
        pygame.sprite.Group.__init__(self)
        self.columns = []
        columns, rows = layout
        for i in range(0, columns):
            column_x = topleft[0] + i*64
            enemy_column = EnemyColumn(topleft[0] + i*64)
            for j in range(0, rows):
                new_enemy = EnemySprite(os.path.join("resources", "Enemy.png"), (column_x, topleft[1] + j*64), bullet_group)
                enemy_column.add(new_enemy)
                self.add(new_enemy)
            self.columns.append(enemy_column)

        self.current_direction = +1
        self.left_bound, self.right_bound, self.bottom_bound = bounds
        self.total = columns * rows

    def update(self, score, collisions):
        direction_change = too_low = False
        scale = int(float(self.total)/float(len(self)))
        for i in self.columns:
            x, y = i.update((scale*self.current_direction*self.H_STEP, 0), score, collisions)
            if (len(i.sprites()) == 0):
                self.columns.remove(i)
            elif (y > self.bottom_bound):
                too_low = True
            elif (x < self.left_bound or x > self.right_bound):
                direction_change = True
        if (len(self.columns) == 0):
            return False, True
        elif too_low:
            return False, False
        elif direction_change:
            self.current_direction *= -1
            for i in self.columns:
                i.update((scale*self.current_direction*self.H_STEP, self.V_STEP), score, [])
        return True, True