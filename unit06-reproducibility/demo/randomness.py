# randomness.py: four ways the same code can give different answers
import numpy as np

# (1) no seed: different every run
print("(1) no seed:  ", np.random.default_rng().normal(size=3).round(3))

# (2) seeded generator: identical every run, on every computer
rng = np.random.default_rng(1213)
print("(2) seed 1213:", rng.normal(size=3).round(3))

# (3) the order of a set of strings changes from run to run
print("(3) set order:", {"Wales", "England", "Scotland"})

# (4) floating point addition depends on the order
print("(4) sums:     ", sum([1.0, 1e16, -1e16]), sum([1e16, -1e16, 1.0]))
