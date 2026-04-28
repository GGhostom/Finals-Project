class CipherSpec:
    def __init__(self, name, cipher_type, key_size, block_size, num_rounds):
        self.name = name
        self.cipher_type = cipher_type
        self.key_size = key_size
        self.block_size = block_size
        self.num_rounds = num_rounds

        self.has_sbox = False
        self.has_permutation = False
        self.operations = []