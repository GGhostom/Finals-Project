from file_reader.module_loader import load_cipher_functions
from utils.spec_builder import build_cipher_spec
from utils.key_utils import generate_key

from models.metrics import Metrics
from models.sample_set import SampleSet

from analyzers import statistical, structural, complexity
from analyzers.indistinguishability import compute_indistinguishability
from engine import scorer

MAX_LAYERS = 3


class CipherEnv:
    def __init__(self):
        self.ciphers = load_cipher_functions()
        self.num_actions = len(self.ciphers)
        self.PAD = self.num_actions

        self.cache = {}

        self.reset()

    def reset(self):
        self.sequence = []
        self.keys = []
        return self._get_state()

    def _get_state(self):
        return self.sequence + [self.PAD] * (MAX_LAYERS - len(self.sequence))

    def step(self, action):
        if action in self.sequence:
            return self._get_state(), -50, True

        cipher = self.ciphers[action]
        key = generate_key(cipher)

        self.sequence.append(action)
        self.keys.append(key)

        done = len(self.sequence) >= MAX_LAYERS

        if done:
            reward = self.evaluate_sequence()
        else:
            reward = 0

        return self._get_state(), reward, done

    def evaluate_sequence(self):
        key = tuple(self.sequence)

        if key in self.cache:
            return self.cache[key]

        samples = SampleSet()

        def layered_encrypt(x):
            for idx, k in zip(self.sequence, self.keys):
                x = self.ciphers[idx](x, k)
            return x

        for i in range(32):
            pt = i
            ct = layered_encrypt(pt)
            samples.add(format(pt, "08b"), format(ct, "08b"))

        metrics = Metrics()

        metrics.avalanche_score = statistical.compute_avalanche(
            samples, self.ciphers[self.sequence[0]],  # representative
            self.ciphers[self.sequence[0]]
        )

        metrics.entropy = statistical.compute_entropy(
            [ct for _, ct in samples.pairs]
        )

        total_key_size = len(self.keys) * 8
        metrics.key_score = structural.key_score(total_key_size)

        time = complexity.brute_force_time(total_key_size)
        metrics.complexity_score = complexity.complexity_score(time)

        metrics.structure_score = len(self.sequence) * 2

        metrics.ind_score = compute_indistinguishability(
            layered_encrypt,
            self.ciphers[self.sequence[0]]
        )

        final = scorer.compute_final_score(metrics)

        reward = final * 10 - len(self.sequence) * 2

        self.cache[key] = reward

        return reward