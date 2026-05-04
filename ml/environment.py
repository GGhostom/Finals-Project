import random
from file_reader.module_loader import load_cipher_functions
from models.metrics import Metrics
from models.sample_set import SampleSet
from engine import scorer
from analyzers import statistical, complexity
from analyzers.ind_cpa import compute_ind_cpa
from utils.key_utils import generate_key_for_cipher


class CipherEnv:
    def __init__(self, max_layers=3):
        self.ciphers = load_cipher_functions()
        self.num_actions = len(self.ciphers)
        # padding token
        self.PAD = self.num_actions
        self.max_layers = max_layers
        # cache: sequence → score
        self.cache = {}
        self.reset()

    def reset(self):
        self.sequence = []
        return self._get_state()

    def _get_state(self):
        return self.sequence + [self.PAD] * (self.max_layers - len(self.sequence))

    def step(self, action):
        if action in self.sequence:
            return self._get_state(), -10, True
        self.sequence.append(action)
        done = len(self.sequence) >= self.max_layers
        if done:
            reward = self.evaluate_sequence(self.sequence)
        else:
            reward = 0
        return self._get_state(), reward, done

    def evaluate_sequence(self, sequence):
        #caching
        key_tuple = tuple(sequence)
        if key_tuple in self.cache:
            return self.cache[key_tuple]
        #generate fixed keys for this sequence
        keys = [generate_key_for_cipher(self.ciphers[idx]) for idx in sequence]
        #layered encryption
        def layered_encrypt(x):
            for i, idx in enumerate(sequence):
                cipher = self.ciphers[idx]
                x = cipher(x, keys[i])
            return x
        #--- dataset ---
        pts = [random.randint(0, 255) for _ in range(64)]
        #--- metrics ---
        metrics = Metrics()
        #--- entropy ---
        cts = [layered_encrypt(pt) for pt in pts]
        metrics.entropy = statistical.compute_entropy(
            [format(ct, "08b") for ct in cts]
        )
        #--- avalanche---
        samples = SampleSet()
        for pt in pts:
            ct = layered_encrypt(pt)
            samples.add(format(pt, "08b"), format(ct, "08b"))
        metrics.avalanche_score = statistical.compute_avalanche(
            samples, layered_encrypt
        )
        # ---complexity---
        time = complexity.brute_force_time(8 * len(sequence))
        metrics.complexity_score = complexity.complexity_score(time)
        #--- structure ---
        metrics.structure_score = len(sequence)
        #--- IND-CPA ---
        metrics.ind_score, _ = compute_ind_cpa(layered_encrypt)
        #--- final score ---
        final_score = scorer.compute_final_score(metrics)
        #cache result
        self.cache[key_tuple] = final_score
        return final_score