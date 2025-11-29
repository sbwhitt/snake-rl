import torch

from torch import nn

DEVICE = "cpu"
if torch.cuda.is_available():
    DEVICE = "cuda:0"
elif torch.mps.is_available():
    DEVICE = "mps"

class LinearModel(nn.Module):
    def __init__(self, grid_size: int, num_actions: int):
        super().__init__()
        hidden = 1024
        self.model = nn.Sequential(
            nn.Linear(grid_size**2, hidden),
            nn.LeakyReLU(),
            nn.Linear(hidden, num_actions),
        )
        self.model.to(DEVICE)

    def forward(self, x):
        x = torch.flatten(x, start_dim=1, end_dim=-1)
        return self.model(x)
