import torch
import torch.optim as optim
import torch.nn.functional as F

from ml.environment import CipherEnv
from ml.model import PolicyNet


def train():
    env = CipherEnv()
    model = PolicyNet(env.num_actions)

    optimizer = optim.Adam(model.parameters(), lr=0.01)

    episodes = 300

    for episode in range(episodes):
        state = env.reset()

        log_probs = []
        rewards = []

        done = False

        while not done:
            state_tensor = torch.tensor([state], dtype=torch.long)

            logits = model(state_tensor)
            probs = F.softmax(logits, dim=1)

            dist = torch.distributions.Categorical(probs)
            action = dist.sample()

            log_probs.append(dist.log_prob(action))

            state, reward, done = env.step(action.item())
            rewards.append(reward)

        total_reward = sum(rewards)

        loss = sum([-lp * total_reward for lp in log_probs])

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if episode % 50 == 0:
            print(f"Episode {episode} | Reward: {total_reward:.2f}")

    return model, env