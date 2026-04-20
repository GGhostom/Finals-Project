from file_reader.module_loader import load_cipher_functions
from utils.spec_builder import build_cipher_spec
from models.layered_cipher import LayeredCipher
import json


def create_all_cipher_specs():
    """
    Build CipherSpec objects for all registered cipher functions.

    Returns:
        dict: {cipher_name: CipherSpec}
    """
    cipher_specs = {}

    cipher_functions = load_cipher_functions()

    for func in cipher_functions:
        spec = build_cipher_spec(func)

        # enforce name = file/module name
        module_name = func.__module__.split('.')[-1]
        spec.name = module_name

        cipher_specs[module_name] = spec

    return cipher_specs


def save_cipher_specs_to_file(cipher_specs, path="cipher_specs.json"):
    """
    Save CipherSpec objects to JSON file
    """
    data = {}

    for name, spec in cipher_specs.items():
        data[name] = {
            "cipher_type": spec.cipher_type,
            "key_size": spec.key_size,
            "block_size": spec.block_size,
            "num_rounds": spec.num_rounds,
            "has_sbox": spec.has_sbox,
            "has_permutation": spec.has_permutation,
            "operations": spec.operations,
        }

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def create_layered_cipher(name, cipher_names, all_specs):
    specs = [all_specs[n] for n in cipher_names]
    return LayeredCipher(name, specs)