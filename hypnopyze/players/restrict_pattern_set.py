from numpy.random import RandomState
from math import ceil


# Randomly picks some subset of patterns
#  - amount should be in [0, 1]
def restrict_pattern_set(patterns, amount: float, prng: RandomState):
    if not 0.0 < amount <= 1.0:
        return []

    count = int(ceil(len(patterns) * amount))
    if count == len(patterns):
        return patterns

    return prng.choice(patterns, replace=False, size=count)
