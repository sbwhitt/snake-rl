import random
import math
import static.colors as colors

from torch import zeros
from pygame import Color
from utils.point import Point

class Snake:
    def __init__(self, grid_size=10, tail_length=1):
        self.grid_size = grid_size
        self.tail: list[Point] = [
            Point(self.grid_size//2, self.grid_size//2),
        ] + [Point(self.grid_size//2, (self.grid_size//2)+i) for i in range(1, tail_length+1)]
        self.last_dir = Point(0, -1)
        self.score = 0
        self.pellet = self._spawn_pellet()

        self.win_reward = 10.
        self.eat_reward = 3
        self.move_reward = -0.2
        self.oob_reward = -3.
        self.lose_reward = -3.

    def _spawn_pellet(self) -> Point | None:
        possible = []
        for i in range(0, self.grid_size):
            for j in range(0, self.grid_size):
                p = Point(i, j)
                if p in self.tail: continue
                possible.append(p)
        return random.choice(possible) if len(possible) > 0 else None

    def _eat(self) -> bool:
        self.pellet = self._spawn_pellet()
        d = self.tail[-1] - self.tail[-2]
        self.tail.append(self.tail[-1] + d)
        self.score += 1

    def move(self, dir: Point):
        if self.tail[0] + dir == self.tail[1]:
            return
        self.last_dir = dir

    def update(self) -> tuple[bool, int]:
        head = self.tail[0] + self.last_dir

        # out of bounds
        if (
            head.x < 0 or
            head.x >= self.grid_size or
            head.y < 0 or
            head.y >= self.grid_size
        ):
            return False

        self.tail = [self.tail[0] + self.last_dir] + self.tail[:-1]
        # ate self
        if head in self.tail[1:]:
            return False

        if self.tail[0] == self.pellet:
            self._eat()
            if self.pellet is None:
                return False
        
        return True

    def get_reward(self, dir: Point) -> float:
        if self.pellet is None:
            return self.win_reward

        next_tail = [self.tail[0] + dir] + self.tail[:-1]
        head = next_tail[0]
        if head in next_tail[1:-1]:
            return self.lose_reward
        if (
            head.x < 0 or
            head.x >= self.grid_size or
            head.y < 0 or
            head.y >= self.grid_size
        ):
            return self.oob_reward
        if head == self.pellet:
            return self.eat_reward

        d = math.sqrt((head.x - self.pellet.x)**2 + (head.y - self.pellet.y)**2)
        return self.move_reward*d

    def get_tiles_to_render(self) -> list[tuple[Point, Color]]:
        # render head, then pellet, then tail
        return [
            (p, colors.GREEN)
            for p in self.tail[1:]
        ] + [
            (self.tail[0], colors.RED),
        ] + [(self.pellet, colors.WHITE)] if self.pellet is not None else []

    def get_state(self):
        state = zeros((1, self.grid_size, self.grid_size))
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                p = Point(r, c)
                if p == self.tail[0]:
                    state[0][c][r] = 1
                elif p in self.tail[1:]:
                    state[0][c][r] = 2
                elif self.pellet is not None and p == self.pellet:
                    state[0][c][r] = 3
        return state
