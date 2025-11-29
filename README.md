# RL Snake Bot

Train a neural network to play the game snake using reinforcement learning via pytorch. The game itself is implemented using pygame and can be played normally by the user.  

Tweak hyperparameters and training settings using the values found in `deep_learner.py`. The settings that are present in the current version of the code are what I found to work the best to produce a semi-competent snake bot. Made for fun and so I could learn more about RL techniques. 

Inspired by:
* https://web.archive.org/web/20180127123915/https://storage.googleapis.com/deepmind-data/assets/papersDeepMindNature14236Paper.pdf
* https://web.archive.org/web/20180407053740/http://neuro.cs.ut.ee/demystifying-deep-reinforcement-learning/
* https://github.com/google-deepmind/dqn/tree/master
* https://en.wikipedia.org/wiki/TD-Gammon#Algorithm_for_play_and_learning

## Rules

The snake has to move in any valid direction during each game update. Valid directions are any direction that does not lead back into the snake's tail (snake moves in the last chosen direction in this case). The game is over and the player loses if the snake's head attempts to go out of bounds or tries to eat its own tail. 

The pellet which the player is trying to eat spawns in a random unoccupied tile somewhere in the grid when the game starts or when it is eaten. If no pellet can be spawned since the board is full of snake, then the player wins.

## Usage

Controls are `W A S D`. Pause or reset the game after losing with `Space`. Exit using `Esc`. Quit the current game using `q`. 

Set whether you want to use a model to play the game or not as well as whether or not to train the model prior to play in the game init args. While training, the model will be saved after each 'epoch' to a `model.pth` file. This file will be loaded as a pre-trained model if it is already present at runtime. 

## How it works 

Using a $n \times n$ grid, the game world is flattened into a $1 \times n^2$ dimensional tensor then fed into the model each time the game updates. The model outputs a 4 dimensional tensor which represents the estimated utility values of the 4 possible actions: Up (0), Down (1), Left (2), Right (3).

Model was trained using MSE loss and RMSProp optimizer. Loss was generated using: ${{argmax}_a}Q(s, a; \theta)$ as the predicted input and $R(s, a) + \gamma{{max}_{a'}}Q(s', a'; \theta)$ as the target (unless $s$ is a terminal state, then it just uses $R(s, a)$), where $Q(s, a; \theta)$ is the estimated utility Q function using model weights $\theta$, $R(s, a)$ is the reward function for taking action $a$ in state $s$, and $\gamma$ is the discount factor. When selecting states during training, model uses an $\epsilon$-greedy approach. 

I primarily experimented with a 5x5 snake grid where the player's head spawns into the center tile with a single tail segment trailing behind them. However, any size grid above 3x3 could be used. 
