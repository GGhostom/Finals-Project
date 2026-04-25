from file_reader.module_loader import load_cipher_functions
from utils.spec_builder import build_cipher_spec

from models.metrics import Metrics
from models.sample_set import SampleSet

from analyzers import statistical, structural, complexity
from engine import scorer, classifier

from ml.train import train

import torch


def analyze_cipher(cipher_func):
    spec = build_cipher_spec(cipher_func)

    samples = SampleSet()

    for i in range(16):
        pt = i
        ct = cipher_func(pt)

        samples.add(format(pt, "08b"), format(ct, "08b"))

    metrics = Metrics()

    metrics.key_score = structural.key_score(spec.key_size)
    metrics.structure_score = structural.structure_score(spec)

    metrics.avalanche_score = statistical.compute_avalanche(
        samples, cipher_func
    )
    metrics.entropy = statistical.compute_entropy(
        [ct for _, ct in samples.pairs]
    )
    time = complexity.brute_force_time(spec.key_size)
    metrics.complexity_score = complexity.complexity_score(time)
    metrics.final_score = scorer.compute_final_score(metrics)
    label = classifier.classify(metrics.final_score)
    return metrics.final_score, label


def main():
    print("\n==== Loading Ciphers ====\n")
    ciphers = load_cipher_functions()
    if not ciphers:
        print("No ciphers found.")
        return

    print("==== Individual Cipher Analysis ====\n")
    for cipher in ciphers:
        score, label = analyze_cipher(cipher)
        print(f"{cipher.__name__}")
        print(f"Score: {score:.2f}")
        print(f"Class: {label}")
        print("-" * 30)

    print("\n==== Training ML ====\n")
    model, env = train()

    print("\n==== Best Layered Cipher ====\n")
    state = env.reset()
    sequence = []
    done = False
    while not done:
        state_tensor = torch.tensor([state], dtype=torch.long)
        logits = model(state_tensor)
        action = torch.argmax(logits, dim=1).item()
        cipher = env.ciphers[action]
        sequence.append(cipher.__name__)
        state, reward, done = env.step(action)
    print(" -> ".join(sequence))
    print(f"\nFinal Score: {reward:.2f}")


if __name__ == "__main__":
    main()