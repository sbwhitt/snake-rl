import static.colors as colors

from pygame import (
    Surface,
    Color,
    Rect,
    draw
)
from utils.point import Point

class Grid:
    def __init__(self, grid_size: int=10):
        self.grid_size = grid_size
        if grid_size < 3:
            raise Exception("Bad grid size")

    def _init_bounds(self, win_size: tuple[int, int]):
        tile_size = min(win_size[0], win_size[1]) // self.grid_size
        x_margin = (win_size[0] - min(win_size[0], win_size[1])) // 2
        y_margin = (win_size[1] - min(win_size[0], win_size[1])) // 2
        return tile_size, x_margin, y_margin

    def render(
        self,
        surface: Surface,
        win_size: tuple[int, int],
        tiles_to_render: list[tuple[Point, Color]]=[],
        show_lines=True
    ):
        tile_size, x_margin, y_margin = self._init_bounds(win_size)
        tiles = tile_size * self.grid_size

        # border
        draw.lines(
            surface,
            colors.WHITE,
            True,
            [
                (x_margin, y_margin),
                (x_margin + tiles, y_margin),
                (x_margin + tiles, y_margin + tiles),
                (x_margin, y_margin + tiles),
            ]
        )

        if show_lines:
            # horizontal grid lines
            for i in range(1, self.grid_size+1):
                offset = i*tile_size
                draw.line(
                    surface,
                    colors.WHITE,
                    (x_margin, y_margin + offset),
                    (x_margin + tiles, y_margin + offset)
                )

            # vertical grid lines
            for i in range(1, self.grid_size+1):
                offset = i*tile_size
                draw.line(
                    surface,
                    colors.WHITE,
                    (x_margin + offset, y_margin),
                    (x_margin + offset, y_margin + tiles)
                )

        # draw populated tiles
        for point, color in tiles_to_render:
            draw.rect(
                surface,
                color,
                Rect(x_margin + (tile_size*point.x), y_margin + (tile_size*point.y), tile_size, tile_size)
            )
