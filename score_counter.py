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

class ScoreCounter(object):
    def __init__(self):
        self.score = 0
    def increment(self):
        self.score += 1

class HighScore(object):
    def __init__(self):
        self.highscore = 0
    def update(self, score):
        if (score > self.highscore):
            self.highscore = score