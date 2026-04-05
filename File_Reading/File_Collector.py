import os
import ast
import shutil


def file_cipher_reader(file_path):
    target_dir = "Cryptography_files"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            node = ast.parse(f.read())
    except (SyntaxError, FileNotFoundError, Exception) as e:
        print(f"Could not process {file_path}: {e}")
        return

    found_functions = {'encrypt': False, 'decrypt': False}


    for item in node.body:
        if isinstance(item, ast.FunctionDef):
            if item.name in found_functions:
                args = [a.arg for a in item.args.args]
                if args == ['msg', 'key']:
                    found_functions[item.name] = True

    if all(found_functions.values()):
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        try:
            shutil.move(file_path, os.path.join(target_dir, os.path.basename(file_path)))
            print(f"Successfully moved: {file_path}")
        except Exception as e:
            print(f"Error moving file: {e}")
    else:
        print(f"File {file_path} does not meet the requirements.")


def file_breaker_reader(file_path):
    target_dir = "cipher_breaker_files"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return
    is_breaker = False

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # 1. Check if it takes exactly 1 argument (the cipher text)
            if len(node.args.args) == 1:
                # 2. Check if the function actually returns something
                for sub_node in ast.walk(node):
                    if isinstance(sub_node, ast.Return) and sub_node.value is not None:
                        is_breaker = True
                        break
        if is_breaker:
            break

    if is_breaker:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        shutil.move(file_path, os.path.join(target_dir, os.path.basename(file_path)))
        print(f"Moved {file_path} to {target_dir}")
    else:
        print(f"File {file_path} does not look like a breaker.")

file_breaker_reader(input("Enter the file path: "))