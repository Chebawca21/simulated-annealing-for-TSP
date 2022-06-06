from simulated_annealing import *

sa = SimulatedAnnealing()

br, bs = sa.anneal()

print("Finished")
print("Best Score: ", bs)
print("Best Route:\n", br)