import torch.nn as nn


class PolicyNet(nn.Module):
    def __init__(self, num_ciphers):
        super().__init__()
        self.embed = nn.Embedding(num_ciphers + 1, 16)
        self.fc = nn.Sequential(
            nn.Linear(16 * 3, 64),
            nn.ReLU(),
            nn.Linear(64, num_ciphers)
        )

    def forward(self, x):
        x = self.embed(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)