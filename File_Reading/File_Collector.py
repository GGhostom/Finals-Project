import os
import shutil
import ast


def register_crypto_module(file_path):
    # 1. Configuration
    target_folder = "Cryptography_files"
    init_file = os.path.join(target_folder, "__init__.py")
    file_name = os.path.basename(file_path)
    module_name = os.path.splitext(file_name)[0]

    # 2. Check if the functions exist using AST
    with open(file_path, "r") as f:
        try:
            node = ast.parse(f.read())
        except SyntaxError:
            print(f"Error: {file_name} has syntax errors.")
            return

    # Extract all function names from the file
    functions = {n.name for n in node.body if isinstance(n, ast.FunctionDef)}

    if "encryption" in functions and "decryption" in functions:
        # 3. Setup the directory
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        # 4. Copy the file
        shutil.copy(file_path, os.path.join(target_folder, file_name))

        # 5. Update or create __init__.py
        update_init_file(init_file, module_name)
        print(f"Successfully registered: {module_name}")
    else:
        print(f"Validation failed: {file_name} is missing required functions.")


def update_init_file(path, module_name):
    all_list = []

    # Read existing __all__ if file exists
    if os.path.exists(path):
        with open(path, "r") as f:
            content = f.read()
            # Simple check to extract existing list (could be improved with AST)
            if "__all__ =" in content:
                try:
                    # Find the list within the string
                    start = content.find("[") + 1
                    end = content.find("]")
                    existing_items = content[start:end].replace("'", "").replace('"', "").split(",")
                    all_list = [i.strip() for i in existing_items if i.strip()]
                except ValueError:
                    all_list = []

    # Add new module if not already there
    if module_name not in all_list:
        all_list.append(module_name)

    # Write back to __init__.py
    with open(path, "w") as f:
        f.write(f"__all__ = {all_list}\n")

# Example Usage:
register_crypto_module(input("Enter File: "))