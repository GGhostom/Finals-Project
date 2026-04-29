import torch
import torch.nn as nn


class PolicyNet(nn.Module):
    def __init__(self, num_actions, max_layers, embed_dim=16):
        super().__init__()

        self.max_layers = max_layers
        self.embed_dim = embed_dim

        # +1 for PAD token
        self.embed = nn.Embedding(num_actions + 1, embed_dim)

        # 🔥 dynamic input size
        input_size = embed_dim * max_layers

        self.fc = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, num_actions)
        )

    def forward(self, x):
        x = self.embed(x)          # (batch, layers, embed_dim)
        x = x.view(x.size(0), -1)  # flatten
        return self.fc(x)