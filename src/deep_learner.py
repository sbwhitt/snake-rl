import os
import time
import torch
import random

from snake import Snake
from utils.point import Point
from models import LinearModel

class DeepLearner:
    """
    References:
    * https://web.archive.org/web/20180407053740/http://neuro.cs.ut.ee/demystifying-deep-reinforcement-learning/
    * https://web.archive.org/web/20180127123915/https://storage.googleapis.com/deepmind-data/assets/papers/DeepMindNature14236Paper.pdf
    * https://github.com/google-deepmind/dqn/tree/master
    * https://en.wikipedia.org/wiki/TD-Gammon#Algorithm_for_play_and_learning
    """
    def __init__(self, grid_size=10):
        self.grid_size = grid_size
        self.snake = None
        self.actions = {
            0: Point(0, -1),
            1: Point(0, 1),
            2: Point(-1, 0),
            3: Point(1, 0)
        }
    
        self.model = LinearModel(self.grid_size, len(self.actions))
        if os.path.exists("model.pth"):
            print("loading existing model")
            self.model.load_state_dict(torch.load("model.pth"))
        print(f"model params: {sum([p.numel() for p in self.model.parameters()])}")

        self.lr = 0.00025
        self.gamma = 0.3
        self.epsilon = 0.99
        self.ep_red_rate = 0.99
        self.ep_floor = 0.1

        self.loss_fn = torch.functional.F.mse_loss
        self.optim = torch.optim.RMSprop(self.model.parameters(), lr=self.lr)

    def _backpropagate(self, loss: torch.Tensor):
        self.optim.zero_grad()
        loss.backward()
        self.optim.step()

    def _step(self):
        s_0 = self.snake.get_state()
        pred = torch.flatten(self.model(s_0))

        a = int(torch.argmax(pred))
        if random.random() < self.epsilon:
            a = random.randint(0, len(self.actions)-1)
            if self.epsilon*self.ep_red_rate > self.ep_floor:
                self.epsilon *= self.ep_red_rate

        move_dir = self.actions[a]
        r = self.snake.get_reward(move_dir)

        self.snake.move(move_dir)
        alive = self.snake.update()
        s_1 = self.snake.get_state()

        target = torch.flatten(self.model(s_1))
        target = torch.max(target)
        target = r + (self.gamma*target*(1 if alive else 0))

        loss = self.loss_fn(pred[a], target)
        self._backpropagate(loss)

        return loss.item(), alive

    def update(self, snake: Snake):
        pred = torch.flatten(self.model(snake.get_state()))
        a = int(torch.argmax(pred))

        # for infinite loops
        if random.random() < 0.01:
            a = random.randint(0, len(self.actions)-1)
            if self.epsilon*self.ep_red_rate > self.ep_floor:
                self.epsilon *= self.ep_red_rate

        dir = self.actions[a]
        snake.move(dir)

    def train(self):
        print("training...")
        epochs = 10
        games = 10000
        timeout_turns = 300
        self.model.train()
        for epoch in range(epochs):
            start = time.time()
            epoch_loss = 0
            score = 0
            total_turns = 0
            timeouts = 0
            for game in range(games):
                alive = True
                game_loss = 0
                current_turns = 0
                self.snake = Snake(self.grid_size)
                while alive and current_turns < timeout_turns:
                    loss, alive = self._step()
                    game_loss += loss
                    current_turns += 1
                if current_turns == timeout_turns:
                    timeouts += 1
                epoch_loss += game_loss / current_turns
                score += self.snake.score
                total_turns += current_turns
            self.epsilon = 0.99
            print(f"epoch {epoch+1} ended with avg loss: {epoch_loss/games:.8f}; avg score: {score/games:.3f}; avg turns: {total_turns/games:.3f} after {time.time()-start:.2f} seconds; {(timeouts/games)*100:.2f}% timeouts")
            torch.save(self.model.state_dict(), 'model.pth')
        self.model.eval()
