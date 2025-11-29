import pygame
import static.colors as colors
import static.inp_codes as inp_codes
import settings as settings
from controls.keys import Keys

from utils.point import Point
from grid import Grid
from snake import Snake
from deep_learner import DeepLearner

class Game:
    def __init__(self, use_learner=True, train=True) -> None:
        self.grid_size = 5
        self.grid = Grid(grid_size=self.grid_size)
        self.snake = Snake(grid_size=self.grid_size)

        self.use_learner = use_learner
        if self.use_learner:
            self.learner = DeepLearner(grid_size=self.grid_size)
            if train:
                self.learner.train()
            self.learner.snake = self.snake

        self.keys = Keys()
        self.surface = pygame.display.set_mode(
            settings.WIN_SIZE,
            pygame.RESIZABLE | pygame.DOUBLEBUF)

        self.clock = pygame.time.Clock()
        self.update_timer = 0
        self.update_interval = 250

        self.running = True
        self.paused = True
        self.new_game = False

    def on_init(self) -> None:
        pass

    def on_execute(self) -> None:
        self.on_init()

        while self.running:
            dt = self.clock.tick_busy_loop(settings.FRAME_RATE)
            for event in pygame.event.get():
                self.handle_event(event)
            if not self.paused: self.update(dt)
            self.render()

        self.on_cleanup()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            self.keys.handle_down(event.key)
            self.handle_key(event.key)
        elif event.type == pygame.KEYUP:
            self.keys.handle_up(event.key)
        elif event.type == pygame.WINDOWRESIZED:
            settings.WIN_SIZE = (event.x, event.y)
        else:
            self._handle_custom_event(event)

    def _handle_custom_event(self, event: pygame.event.Event):
        pass

    def handle_key(self, key: int) -> None:
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_SPACE:
            self.paused = not self.paused
        elif key == pygame.K_q:
            self.new_game = True
            self.paused = True

    def update(self, dt: int) -> None:
        self.update_timer += dt

        if self.new_game:
            self.snake = Snake(self.grid_size)
            if self.use_learner:
                self.learner.snake = self.snake
            self.new_game = False

        if not self.use_learner:
            if self.keys.is_down(inp_codes.KEY_W):
                self.snake.move(Point(0, -1))
            elif self.keys.is_down(inp_codes.KEY_S):
                self.snake.move(Point(0, 1))
            elif self.keys.is_down(inp_codes.KEY_A):
                self.snake.move(Point(-1, 0))
            elif self.keys.is_down(inp_codes.KEY_D):
                self.snake.move(Point(1, 0))

        if self.update_timer >= self.update_interval:
            self.update_timer = 0
            alive = True
            if self.use_learner:
                self.learner.update(self.snake)
            alive = self.snake.update()
            if not alive:
                self.paused = True
                self.new_game = True

    def render(self) -> None:
        self.surface.fill(colors.BLACK)
        self.grid.render(
            self.surface,
            settings.WIN_SIZE,
            tiles_to_render=self.snake.get_tiles_to_render()
        )
        
        pygame.display.flip()

    def on_cleanup(self) -> None:
        pass


if __name__ == "__main__":
    Game().on_execute()
