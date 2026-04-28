from file_reader.module_loader import load_cipher_functions
from utils.spec_builder import build_cipher_spec

from models.metrics import Metrics
from models.sample_set import SampleSet

from analyzers import statistical, structural, complexity
from analyzers.indistinguishability import compute_indistinguishability

from engine import scorer, classifier

from ml.train import train


# =========================
# ANALYZE SINGLE CIPHER
# =========================
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

    # 🔥 NEW ML metric
    metrics.ind_score = compute_indistinguishability(cipher_func)

    metrics.final_score = scorer.compute_final_score(metrics)

    label = classifier.classify(metrics.final_score)

    return metrics, label


# =========================
# MAIN PIPELINE
# =========================
def main():
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

    model, env, best_sequence, best_reward = train()

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


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()