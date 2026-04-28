from file_reader.module_loader import load_cipher_functions

from models.metrics import Metrics
from models.sample_set import SampleSet

from analyzers import statistical, structural, complexity
from engine import scorer, classifier

from ml.train import train

import torch


# =========================
# INDIVIDUAL ANALYSIS
# =========================

def analyze_cipher(cipher):
    samples = SampleSet()

    key = 42  # fixed analysis key (deterministic evaluation)

    for i in range(16):
        pt = i
        ct = cipher.encrypt(pt, key)
        samples.add(format(pt, "08b"), format(ct, "08b"))

    metrics = Metrics()

    metrics.key_score = structural.key_score(
        8 if cipher.key_type == "int" else 16
    )

    metrics.structure_score = structural.structure_score(cipher)

    metrics.avalanche_score = statistical.compute_avalanche(
        samples,
        cipher.encrypt,
        key
    )

    metrics.entropy = statistical.compute_entropy(
        [ct for _, ct in samples.pairs]
    )

    time = complexity.brute_force_time(metrics.key_score)
    metrics.complexity_score = complexity.complexity_score(time)

    metrics.final_score = scorer.compute_final_score(metrics)

    label = classifier.classify(metrics.final_score)

    return metrics.final_score, label


# =========================
# MAIN
# =========================

def main():
    print("\n==== Loading Ciphers ====\n")

    ciphers = load_cipher_functions()

    if not ciphers:
        print("No ciphers found.")
        return

    print("\n==== Individual Cipher Analysis ====\n")

    best_single = None
    best_score = -1

    for cipher in ciphers:

        try:
            score, label = analyze_cipher(cipher)

            print(f"{cipher.name}")
            print(f"Score: {score:.2f}")
            print(f"Class: {label}")
            print("-" * 30)

            if score > best_score:
                best_score = score
                best_single = cipher

        except Exception as e:
            print(f"[ERROR] {cipher.name}: {e}")

    # =========================
    # ML TRAINING PHASE
    # =========================

    print("\n==== Training ML ====\n")

    model, env = train(ciphers)

    print("\n==== Best Layered Cipher ====\n")

    state = env.reset()
    sequence = []

    done = False

    while not done:

        state_tensor = torch.tensor([state], dtype=torch.long)

        logits = model(state_tensor)
        action = torch.argmax(logits, dim=1).item()

        cipher = env.ciphers[action]
        sequence.append(cipher.name)

        state, reward, done = env.step(action)

    print(" -> ".join(sequence))
    print(f"\nFinal Layer Score: {reward:.2f}")

    print(f"\nBest Single Cipher: {best_single.name} ({best_score:.2f})")


if __name__ == "__main__":
    main()