import random
import torch
import torch.nn as nn
import torch.optim as optim


def int_to_bits(x):
    return [(x >> i) & 1 for i in range(8)]


class SmallClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(8, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x)


def sample_pairs(n=2000):
    A = [0 for _ in range(n)]
    B = [random.randint(0, 255) for _ in range(n)]
    return A, B


def build_dataset(encrypt_func, n=2000):
    A, B = sample_pairs(n)
    X = []
    y = []
    for pt in A:
        X.append(int_to_bits(encrypt_func(pt)))
        y.append(0)
    for pt in B:
        X.append(int_to_bits(encrypt_func(pt)))
        y.append(1)
    return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32).unsqueeze(1)


def train_and_eval(encrypt_func):
    X, y = build_dataset(encrypt_func)
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    model = SmallClassifier()
    optimizer = optim.Adam(model.parameters(), lr=0.005)
    criterion = nn.BCELoss()
    for _ in range(120):
        preds = model(X_train)
        loss = criterion(preds, y_train)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    with torch.no_grad():
        preds = model(X_test)
        predicted = (preds > 0.5).float()
        acc = (predicted == y_test).float().mean().item()
    advantage = abs(acc - 0.5) * 2
    score = 1 - advantage
    return score, acc


def compute_ind_cpa(encrypt_func, repeats=3):
    scores = []
    accs = []
    for _ in range(repeats):
        s, a = train_and_eval(encrypt_func)
        scores.append(s)
        accs.append(a)
    return sum(scores) / len(scores), sum(accs) / len(accs)