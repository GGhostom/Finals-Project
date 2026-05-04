from models.cipher_spec import CipherSpec
import inspect


def build_cipher_spec(encrypt_func, hints=None):
    if hints is None:
        hints = {}

    # merge decorator metadata
    if hasattr(encrypt_func, "_cipher_meta"):
        hints = {**encrypt_func._cipher_meta, **hints}
    name = encrypt_func.__name__
    cipher_type = hints.get("cipher_type", "unknown")
    key_size = hints.get("key_size", 0)
    block_size = hints.get("block_size", 0)
    num_rounds = hints.get("num_rounds", 0)
    spec = CipherSpec(name, cipher_type, key_size, block_size, num_rounds)
    detect_operations(encrypt_func, spec)
    spec.has_sbox = hints.get("has_sbox", False)
    spec.has_permutation = hints.get("has_permutation", False)
    return spec


def detect_operations(func, spec):
    try:
        source = inspect.getsource(func)
    except:
        return
    if "^" in source:
        spec.operations.append("xor")
    if "+" in source:
        spec.operations.append("add")
    if "<<" in source or ">>" in source:
        spec.operations.append("shift")
    if "%" in source:
        spec.operations.append("mod")
    if "[" in source and "]" in source:
        spec.has_sbox = True


# def cipher_metadata(**meta):
#     def wrapper(func):
#         func._cipher_meta = meta
#         return func
#     return wrapper