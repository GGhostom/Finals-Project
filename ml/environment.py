from file_reader.module_loader import load_cipher_functions
from utils.spec_builder import build_cipher_spec

from models.metrics import Metrics
from models.sample_set import SampleSet

from analyzers import statistical, structural, complexity
from engine import scorer

MAX_LAYERS = 3


class CipherEnv:
    def __init__(self):
        self.ciphers = load_cipher_functions()
        self.num_actions = len(self.ciphers)
        self.PAD = self.num_actions  # padding index
        self.reset()

    def reset(self):
        self.sequence = []  # store indices, not functions
        return self._get_state()

    def _get_state(self):
        return self.sequence + [self.PAD] * (MAX_LAYERS - len(self.sequence))

    def step(self, action):
        self.sequence.append(action)

        done = len(self.sequence) >= MAX_LAYERS

        if done:
            reward = self.evaluate_sequence(self.sequence)
        else:
            reward = 0

        return self._get_state(), reward, done

    def evaluate_sequence(self, sequence):
        samples = SampleSet()

        for i in range(16):
            pt = i
            ct = pt

            for idx in sequence:
                cipher = self.ciphers[idx]
                ct = cipher(ct)

            samples.add(format(pt, "08b"), format(ct, "08b"))

        metrics = Metrics()

        # use first cipher spec as approximation
        first_cipher = self.ciphers[sequence[0]]
        spec = build_cipher_spec(first_cipher)

        metrics.key_score = structural.key_score(spec.key_size)
        metrics.structure_score = structural.structure_score(spec)

        metrics.avalanche_score = statistical.compute_avalanche(
            samples, lambda x: x
        )

        metrics.entropy = statistical.compute_entropy(
            [ct for _, ct in samples.pairs]
        )

        time = complexity.brute_force_time(spec.key_size)
        metrics.complexity_score = complexity.complexity_score(time)

        final = scorer.compute_final_score(metrics)

        return final * 10  # scaled reward for better learning