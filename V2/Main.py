from models.cipher_spec import CipherSpec
from models.sample_set import SampleSet
from models.metrics import Metrics
from analyzers import statistical, structural, complexity
from engine import scorer, classifier


def main():
    spec = CipherSpec("ToyCipher", "block", 48, 64, 6)
    spec.has_sbox = True
    spec.has_permutation = True
    spec.operations = ["xor"]
    samples = SampleSet()
    samples.add("0101", "1100")

    metrics = Metrics()

    # Structural
    metrics.key_score = structural.key_score(spec.key_size)
    metrics.structure_score = structural.structure_score(spec)

    # Statistical
    metrics.avalanche_score = statistical.compute_avalanche(samples, encrypt_func=lambda x: x)
    metrics.entropy = statistical.compute_entropy([ct for _, ct in samples.pairs])

    # Complexity
    time = complexity.brute_force_time(spec.key_size)
    metrics.complexity_score = complexity.complexity_score(time)

    # Final
    metrics.final_score = scorer.compute_final_score(metrics)
    result = classifier.classify(metrics.final_score)

    print("Final Score:", metrics.final_score)
    print("Classification:", result)


if __name__ == "__main__":
    main()