class SampleSet:
    def __init__(self):
        self.pairs = []  # list of (plaintext, ciphertext)

    def add(self, pt, ct):
        self.pairs.append((pt, ct))