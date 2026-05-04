from file_reader.module_loader import load_cipher_functions
from models.metrics import Metrics
from models.sample_set import SampleSet
from analyzers import statistical, complexity
from engine import scorer, classifier
from ml.train import train
from analyzers.ind_cpa import compute_ind_cpa
from utils.key_utils import generate_key_for_cipher


# =========================
# ANALYZE SINGLE CIPHER
# =========================


def analyze_cipher(cipher_func):
    key = generate_key_for_cipher(cipher_func)
    def f(x):
        return cipher_func(x, key)
    samples = SampleSet()
    for i in range(32):
        pt = i
        ct = f(pt)
        samples.add(format(pt, "08b"), format(ct, "08b"))
    metrics = Metrics()
    metrics.avalanche_score = statistical.compute_avalanche(samples, f)
    metrics.entropy = statistical.compute_entropy([ct for _, ct in samples.pairs])
    time = complexity.brute_force_time(8)
    metrics.complexity_score = complexity.complexity_score(time)
    metrics.structure_score = 2
    metrics.ind_score, metrics.ind_acc = compute_ind_cpa(f)
    metrics.final_score = scorer.compute_final_score(metrics)
    label = classifier.classify(metrics.final_score)
    return metrics, label


# =========================
# MAIN PIPELINE
# =========================
def main():
    try:
        max_layers = int(input("Enter number of cipher layers (e.g. 2-5): "))
        if max_layers <= 0:
            raise ValueError
    except:
        print("Invalid input, defaulting to 3 layers.")
        max_layers = 3
    print("\n==== Loading Ciphers ====\n")

    ciphers = load_cipher_functions()
    if not ciphers:
        print("No ciphers found.")
        return

    # =========================
    # Individual analysis
    # =========================
    print("==== Individual Cipher Analysis ====\n")
    best_single = None
    best_score = -1
    for cipher in ciphers:
        metrics, label = analyze_cipher(cipher)
        print(f"{cipher.__name__}")
        print(f"Score: {metrics.final_score:.2f}")
        print(f"Class: {label}")
        print(f"Entropy: {metrics.entropy:.3f}")
        print(f"Avalanche: {metrics.avalanche_score:.3f}")
        print(f"IND Score: {metrics.ind_score:.3f}")
        print("-" * 40)
        if metrics.final_score > best_score:
            best_score = metrics.final_score
            best_single = cipher

    # =========================
    # Train ML
    # =========================
    print("\n==== Training ML ====\n")
    model, env, best_sequence, best_reward = train(max_layers)

    # =========================
    # Output best layered cipher
    # =========================
    print("\n==== Best Layered Cipher ====\n")

    if best_sequence:
        names = [env.ciphers[i].__name__ for i in best_sequence]
        print(" -> ".join(names))
        print(f"\nFinal Layer Score: {best_reward:.2f}")
    else:
        print("No valid sequence found.")

    # =========================
    # Compare with single cipher
    # =========================
    print(f"\nBest Single Cipher: {best_single.__name__} ({best_score:.2f})")


if __name__ == "__main__":
    main()