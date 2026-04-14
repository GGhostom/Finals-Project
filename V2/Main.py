from utils.spec_builder import build_cipher_spec
from models.sample_set import SampleSet
from models.metrics import Metrics
from analyzers import statistical, structural, complexity
from engine import scorer, classifier

def toy_encrypt(x):
    return x ^ 0b1010

def main():
    spec = build_cipher_spec(
        toy_encrypt,
        hints={
            "cipher_type": "block",
            "key_size": 4,
            "block_size": 4,
            "num_rounds": 1
        }
    )

    samples = SampleSet()
    samples.add("0101", "1100")

    metrics = Metrics()

    metrics.key_score = structural.key_score(spec.key_size)
    metrics.structure_score = structural.structure_score(spec)

    metrics.avalanche_score = statistical.compute_avalanche(samples, toy_encrypt)
    metrics.entropy = statistical.compute_entropy([ct for _, ct in samples.pairs])

    time = complexity.brute_force_time(spec.key_size)
    metrics.complexity_score = complexity.complexity_score(time)

    metrics.final_score = scorer.compute_final_score(metrics)
    result = classifier.classify(metrics.final_score)

    print(spec.name)
    print(metrics.final_score)
    print(result)


if __name__ == "__main__":
    main()