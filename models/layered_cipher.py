class LayeredCipher:
    def __init__(self, name, cipher_specs):
        self.name = name
        self.cipher_specs = cipher_specs  # list of CipherSpec

        self.metrics = None
        self.final_score = 0
        self.classification = None