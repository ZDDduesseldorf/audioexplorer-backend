import numpy as np

# Wir sollten den Daten normalizieren
# Wir bekommen das in % (wie 78%)


def normalize_scores(scores):

    min_score = np.min(scores)
    max_score = np.max(scores)

    if max_score - min_score == 0:
        return np.zeros(len(scores))

    normalized = ((scores - min_score) / (max_score - min_score)) * 100

    return normalized
