import os
import shutil
import ast


def register_crypto_module(file_path):
    target_folder = "Cryptography_files"
    init_file = os.path.join(target_folder, "__init__.py")
    file_name = os.path.basename(file_path)
    module_name = os.path.splitext(file_name)[0]

    with open(file_path, "r") as f:
        try:
            node = ast.parse(f.read())
        except SyntaxError:
            print(f"Error: {file_name} has syntax errors.")
            return

    functions = {n.name for n in node.body if isinstance(n, ast.FunctionDef)}
    if "encryption" in functions and "decryption" in functions:
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        shutil.copy(file_path, os.path.join(target_folder, file_name))
        update_init_file(init_file, module_name)
        print(f"Successfully registered: {module_name}")
    else:
        print(f"Validation failed: {file_name} is missing required functions.")


def update_init_file(path, module_name):
    all_list = []
    if os.path.exists(path):
        with open(path, "r") as f:
            content = f.read()
            if "__all__ =" in content:
                try:
                    start = content.find("[") + 1
                    end = content.find("]")
                    existing_items = content[start:end].replace("'", "").replace('"', "").split(",")
                    all_list = [i.strip() for i in existing_items if i.strip()]
                except ValueError:
                    all_list = []
    if module_name not in all_list:
        all_list.append(module_name)
    with open(path, "w") as f:
        f.write(f"__all__ = {all_list}\n")


# register_crypto_module(input("Enter File: "))