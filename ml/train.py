import torch
import torch.optim as optim
import torch.nn.functional as F
import random
import numpy as np

from ml.environment import CipherEnv
from ml.model import PolicyNet


def train():
    torch.manual_seed(42)
    random.seed(42)
    np.random.seed(42)

    env = CipherEnv()
    model = PolicyNet(env.num_actions)

    optimizer = optim.Adam(model.parameters(), lr=0.01)

    episodes = 500

    best_reward = float("-inf")
    best_sequence = None

    for episode in range(episodes):
        state = env.reset()

        log_probs = []
        rewards = []

        done = False

        while not done:
            state_tensor = torch.tensor([state], dtype=torch.long)

            logits = model(state_tensor)
            probs = F.softmax(logits, dim=1)

            epsilon = max(0.1, 1 - episode / episodes)

            if random.random() < epsilon:
                action = torch.randint(0, env.num_actions, (1,))
                log_prob = torch.log(probs[0][action])
            else:
                action = torch.argmax(probs, dim=1)
                log_prob = torch.log(probs[0][action])

            log_probs.append(log_prob)

            state, reward, done = env.step(action.item())
            rewards.append(reward)

        total_reward = sum(rewards)

        if total_reward > best_reward:
            best_reward = total_reward
            best_sequence = env.sequence.copy()

        loss = sum([-lp * total_reward for lp in log_probs])

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if episode % 50 == 0:
            print(f"Episode {episode} | Reward: {total_reward:.2f}")

    print("\n==== Training Complete ====")
    print(f"Best Reward Found: {best_reward:.2f}")

    if best_sequence:
        names = [env.ciphers[i].__name__ for i in best_sequence]
        print("Best Sequence:", " -> ".join(names))

    return model, env, best_sequence, best_reward