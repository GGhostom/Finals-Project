import random

# ### Version 1
#
# def foo(x,y,z):
#     return 6*x**3 + 9*y**2 + 90*z
#
# def fitness(x,y,z):
#     ans = foo(x,y,z)
#     if ans == 0:
#         return 999999
#     else:
#         return abs(1/ans)
#
# # solutions
# solutions = []
# for s in range(1000):
#     solutions.append((random.uniform(0,10000),
#                       random.uniform(0,10000),
#                       random.uniform(0,10000)
#     ))
#
# for i in range(1000):
#     rankedSolutions = []
#     for s in solutions:
#         rankedSolutions.append((fitness(s[0],s[1],s[2]),s))
#     rankedSolutions.sort()
#     rankedSolutions.reverse()
#     print(f"=== gen {i} best solution ===")
#     print(rankedSolutions[0])
#     if rankedSolutions[0][0] > 999:
#         break
#
#     bestSolution = rankedSolutions[:100]
#     elements = []
#     for s in bestSolution:
#         elements.append((s[1][0]))
#         elements.append((s[1][1]))
#         elements.append((s[1][2]))
#     newGen = []
#     for _ in range(1000):
#         e1 = random.choice(elements) * random.uniform(0.99,1.01)
#         e2 = random.choice(elements) * random.uniform(0.99,1.01)
#         e3 = random.choice(elements) * random.uniform(0.99,1.01)
#         newGen.append((e1,e2,e3))
#     solutions = newGen

def xor_op(data): return "xor_applied"
def shift_op(data): return "shift_applied"
def swap_op(data): return "swap_applied"
def reverse_op(data): return "reverse_applied"


FUNCTION_POOL = [xor_op, shift_op, swap_op, reverse_op]
LAYER_DEPTH = 5

def run_cipher_layer(sequence, data):
    for func in sequence:
        data = func(data)
    return data

def get_cipher_strength(sequence):
    return random.uniform(0, 1000)


# --- Main ---
solutions = []
for _ in range(100):
    individual = [random.choice(FUNCTION_POOL) for _ in range(LAYER_DEPTH)]
    solutions.append(individual)

for gen in range(1000):
    ranked_solutions = []
    for s in solutions:
        score = get_cipher_strength(s)
        ranked_solutions.append((score, s))
    ranked_solutions.sort(key=lambda x: x[0], reverse=True)
    print(f"Gen {gen} Best Strength: {ranked_solutions[0][0]}")
    if ranked_solutions[0][0] > 9999:
        break
    best_ones = ranked_solutions[:20]

    new_gen = []
    for _ in range(100):
        p1 = random.choice(best_ones)[1]
        p2 = random.choice(best_ones)[1]
        split = LAYER_DEPTH // 2
        child = p1[:split] + p2[split:]
        if random.random() < 0.1:
            child[random.randint(0, LAYER_DEPTH - 1)] = random.choice(FUNCTION_POOL)
        new_gen.append(child)
    solutions = new_gen


best_layer = ranked_solutions[0][1]
print(f"Optimized Layer Sequence: {[f.__name__ for f in best_layer]}")
