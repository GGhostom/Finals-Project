import importlib
from file_reader.cryptography_files import __all__


def load_cipher_functions():
    cipher_functions = []

    for module_name in __all__:
        module = importlib.import_module(
            f"file_reader.cryptography_files.{module_name}"
        )

        if hasattr(module, "encryption"):
            func = getattr(module, "encryption")

            # 🔥 attach module name
            func.__name__ = module_name

            cipher_functions.append(func)

    return cipher_functions