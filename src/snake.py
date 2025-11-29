import random
import static.colors as colors

from pygame import Color
from utils.point import Point

class Snake:
    def __init__(self, grid_size=10):
        self.grid_size = grid_size
        self.tail: list[Point] = [
            Point(self.grid_size//2, self.grid_size//2),
            Point(self.grid_size//2, (self.grid_size//2)+1),
            # Point(self.grid_size//2, (self.grid_size//2)+2),
            # Point(self.grid_size//2, (self.grid_size//2)+3),
            # Point(self.grid_size//2, (self.grid_size//2)+4)
        ]
        self.last_dir = Point(0, -1)
        self.pellet = Point(5, 5)

    def _eat(self):
        self.pellet = Point(random.randint(1, self.grid_size-2), random.randint(1, self.grid_size-2))
        d = self.tail[-1] - self.tail[-2]
        self.tail.append(self.tail[-1] + d)

    def move(self, dir: Point):
        if self.tail[0] + dir in self.tail:
            return
        self.last_dir = dir

    def update(self) -> bool:
        last = self.tail[0]
        self.tail[0] = self.tail[0] + self.last_dir
        for i, t in enumerate(self.tail):
            if i == 0: continue
            self.tail[i] = last
            last = t

        if (
            self.tail[0].x < 0 or
            self.tail[0].x >= self.grid_size or
            self.tail[0].y < 0 or
            self.tail[0].y >= self.grid_size or
            self.tail[0] in self.tail[1:]
        ):
            return False

        if self.tail[0] == self.pellet:
            self._eat()

        return True

    def get_tiles_to_render(self) -> list[tuple[Point, Color]]:
        # render head, then pellet, then tail
        return [
            (p, colors.GREEN)
            for p in self.tail[1:]
        ] + [
            (self.tail[0], colors.RED),
            (self.pellet, colors.WHITE)
        ]
