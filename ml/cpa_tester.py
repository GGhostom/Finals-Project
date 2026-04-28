import torch
import torch.nn as nn
import torch.optim as optim
import random

from ml.classifier_model import CipherClassifier
from utils.key_utils import generate_key


def int_to_bits(x):
    return [(x >> i) & 1 for i in range(8)]


def generate_dataset(encrypt_func, cipher_func, n=1000):
    data = []
    labels = []

    key = generate_key(cipher_func)

    for _ in range(n):
        pt = random.randint(0, 255)
        ct = encrypt_func(pt, key)
        data.append(ct)
        labels.append(0)

    for _ in range(n):
        pt = random.randint(0, 255)
        ct = encrypt_func(pt, key)
        data.append(ct)
        labels.append(1)

    return data, labels


def train_classifier(encrypt_func, cipher_func):
    data, labels = generate_dataset(encrypt_func, cipher_func)

    X = torch.tensor(
        [int_to_bits(x) for x in data],
        dtype=torch.float32
    )

    y = torch.tensor(labels, dtype=torch.float32).unsqueeze(1)

    model = CipherClassifier()
    optimizer = optim.Adam(model.parameters(), lr=0.005)
    criterion = nn.BCELoss()

    for _ in range(100):
        preds = model(X)
        loss = criterion(preds, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        preds = model(X)
        predicted = (preds > 0.5).float()
        acc = (predicted == y).float().mean().item()

    return acc