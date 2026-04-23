import importlib
from file_reader.cryptography_files import __all__


def load_cipher_functions():
    cipher_functions = []

    for module_name in __all__:
        module = importlib.import_module(
            f"file_reader.cryptography_files.{module_name}"
        )

        for attr_name in dir(module):
            if "encrypt" in attr_name:
                func = getattr(module, attr_name)
                if callable(func):
                    cipher_functions.append(func)

    return cipher_functions