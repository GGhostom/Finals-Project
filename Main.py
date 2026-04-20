from utils.spec_registry import create_all_cipher_specs
from file_reader.module_loader import load_cipher_functions
from analyzers.layered_analysis import analyze_layered_cipher


def main():
    specs = create_all_cipher_specs()
    funcs = load_cipher_functions()

    # map name → function
    func_map = {
        f.__module__.split('.')[-1]: f
        for f in funcs
    }

    print("=== SINGLE CIPHERS ===")
    for name, spec in specs.items():
        print(name, "-> key:", spec.key_size)

    print("\n=== LAYERED TEST ===")

    result = analyze_layered_cipher(
        name="combo_cipher",
        cipher_funcs=[
            func_map["toy_spn"],
            func_map["weak_cipher"]
        ],
        cipher_specs=[
            specs["toy_spn"],
            specs["weak_cipher"]
        ]
    )

    print(result)


if __name__ == "__main__":
    main()