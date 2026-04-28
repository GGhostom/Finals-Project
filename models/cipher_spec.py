class CipherSpec:
    def __init__(
        self,
        name,
        encrypt_func,
        key_type="int",
        has_sbox=False,
        has_permutation=False
    ):
        self.name = name
        self.encrypt = encrypt_func
        self.key_type = key_type
        self.has_sbox = has_sbox
        self.has_permutation = has_permutation

    def __repr__(self):
        return (
            f"CipherSpec("
            f"name={self.name}, "
            f"key={self.key_type}, "
            f"sbox={self.has_sbox}, "
            f"perm={self.has_permutation})"
        )