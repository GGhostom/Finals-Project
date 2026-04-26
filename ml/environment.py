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
        self.PAD = self.num_actions
        self.reset()

    def reset(self):
        self.sequence = []
        return self._get_state()

    def _get_state(self):
        return self.sequence + [self.PAD] * (MAX_LAYERS - len(self.sequence))

    def step(self, action):
        # ❌ prevent duplicate cipher usage
        if action in self.sequence:
            return self._get_state(), -50, True

        self.sequence.append(action)

        done = len(self.sequence) >= MAX_LAYERS

        if done:
            reward = self.evaluate_sequence(self.sequence)
        else:
            reward = 0

        return self._get_state(), reward, done

    def evaluate_sequence(self, sequence):
        samples = SampleSet()

        # 🔹 real layered encryption
        def layered_encrypt(x):
            for idx in sequence:
                cipher = self.ciphers[idx]
                x = cipher(x)
            return x

        # generate samples
        for i in range(32):
            pt = i
            ct = layered_encrypt(pt)
            samples.add(format(pt, "08b"), format(ct, "08b"))

        metrics = Metrics()

        # 🔹 statistical (REAL)
        metrics.avalanche_score = statistical.compute_avalanche(
            samples, layered_encrypt
        )

        metrics.entropy = statistical.compute_entropy(
            [ct for _, ct in samples.pairs]
        )

        # 🔹 structural (combined key size)
        total_key_size = 0
        for idx in sequence:
            spec = build_cipher_spec(self.ciphers[idx])
            total_key_size += spec.key_size

        metrics.key_score = structural.key_score(total_key_size)

        # 🔹 complexity
        time = complexity.brute_force_time(total_key_size)
        metrics.complexity_score = complexity.complexity_score(time)

        # 🔹 structure score (simple but meaningful)
        metrics.structure_score = len(sequence) * 2

        final = scorer.compute_final_score(metrics)

        # 🔥 reward shaping
        reward = final * 10 - len(sequence) * 2

        return reward