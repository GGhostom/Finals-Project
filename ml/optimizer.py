import itertools
from ml.feature_extractor import extract_features


def find_best_layering(model, cipher_specs, max_layers=3):
    best_score = -1
    best_combo = None

    names = list(cipher_specs.keys())

    for r in range(2, max_layers + 1):
        for combo in itertools.combinations(names, r):

            features = []

            for name in combo:
                spec = cipher_specs[name]
                features.extend(extract_features(spec))

            predicted_score = model.predict([features])[0]

            if predicted_score > best_score:
                best_score = predicted_score
                best_combo = combo

    return best_combo, best_score