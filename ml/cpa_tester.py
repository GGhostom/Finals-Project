import torch
import torch.nn as nn
import torch.optim as optim
import random
from ml.classifier_model import CipherClassifier


def int_to_bits(x):
    return [(x >> i) & 1 for i in range(8)]


def generate_dataset(encrypt_func, n=1000):
    data = []
    labels = []

    #two independent random distributions
    for _ in range(n):
        pt = random.randint(0, 255)
        ct = encrypt_func(pt)
        data.append(ct)
        labels.append(0)
    for _ in range(n):
        pt = random.randint(0, 255)
        ct = encrypt_func(pt)
        data.append(ct)
        labels.append(1)
    return data, labels


def train_classifier(encrypt_func):
    data, labels = generate_dataset(encrypt_func, n=1000)
    X = torch.tensor(
        [int_to_bits(x) for x in data],
        dtype=torch.float32
    )
    y = torch.tensor(labels, dtype=torch.float32).unsqueeze(1)
    #split train/test
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    model = CipherClassifier()
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.005)
    # more training
    for _ in range(100):
        preds = model(X_train)
        loss = criterion(preds, y_train)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    # evaluation
    with torch.no_grad():
        preds = model(X_test)
        predicted = (preds > 0.5).float()
        accuracy = (predicted == y_test).float().mean().item()
    return accuracy