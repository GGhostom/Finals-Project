import importlib
import os
import sys

from models.cipher_spec import CipherSpec


def load_cipher_functions():
    folder = "file_reader/cryptography_files"
    sys.path.append(folder)

    ciphers = []

    for file in os.listdir(folder):
        if file.endswith(".py") and file != "__init__.py":

            module_name = file[:-3]
            module = importlib.import_module(module_name)

            # ❗ ONLY ACCEPT VALID MODULES
            if not hasattr(module, "encryption"):
                continue

            cipher = CipherSpec(
                name=module_name,
                encrypt_func=module.encryption,
                key_type=getattr(module, "KEY_TYPE", "int"),
                has_sbox=getattr(module, "HAS_SBOX", False),
                has_permutation=getattr(module, "HAS_PERMUTATION", False)
            )

            ciphers.append(cipher)

    return ciphers