import os
import time
import importlib.util


# def run_benchmarks(original_msg, test_key):
#     crypto_dir = "Cryptography_files"
#     breaker_dir = "cipher_breaker_files"
#
#     def get_modules_from_dir(directory):
#         modules = []
#         if not os.path.exists(directory):
#             return modules
#         for filename in os.listdir(directory):
#             if filename.endswith(".py"):
#                 path = os.path.join(directory, filename)
#                 spec = importlib.util.spec_from_file_location(filename[:-3], path)
#                 mod = importlib.util.module_from_spec(spec)
#                 spec.loader.exec_module(mod)
#                 modules.append((filename, mod))
#         return modules
#
#     ciphers = get_modules_from_dir(crypto_dir)
#     breakers = get_modules_from_dir(breaker_dir)
#
#     if not ciphers or not breakers:
#         print("Ensure both folders contain valid .py files!")
#         return
#
#     for c_name, c_mod in ciphers:
#         results = []
#
#         try:
#             encrypted_msg = c_mod.encrypt(original_msg, test_key)
#         except Exception as e:
#             print(f"Error encrypting with {c_name}: {e}")
#             continue
#
#         for b_name, b_mod in breakers:
#             breaker_func = None
#             for attr in dir(b_mod):
#                 obj = getattr(b_mod, attr)
#                 if callable(obj) and not attr.startswith("__"):
#                     import inspect
#                     if len(inspect.signature(obj).parameters) == 1:
#                         breaker_func = obj
#                         break
#
#             if breaker_func:
#                 start_time = time.perf_counter()
#                 try:
#                     result = breaker_func(encrypted_msg)
#                     if str(result) == str(original_msg) or str(result) == str(test_key):
#                         elapsed = time.perf_counter() - start_time
#                         results.append(f"{elapsed:.6f}s")
#                     else:
#                         results.append("Failed")
#                 except Exception:
#                     results.append("Error")
#             else:
#                 results.append("No Func")
#
#         print(f"{c_name}: [{', '.join(results)}]")
#
# # Example Execution:
# # run_benchmarks("SECRET MESSAGE", 5)
