'''
Run simulated annealing for the graph specified in conf/train.json file.
'''

from simulated_annealing import SimulatedAnnealing
from data_loader import DataLoader
import json

if __name__ == '__main__':
    file = open("conf/train.json")
    data = json.load(file)

    dl = DataLoader(data['fileName'], data['solFileName'])
    sa = SimulatedAnnealing(dl.getAdjencyMatrix(), dl.getRoute(), dl.getDim(), K=100000, t0=0.3, tMin=0.16, alpha=0.999995, draw=False, print=True)
    br, bs, et = sa.anneal()
    print("Finished")
    print("Best Score: ", bs)
    print("Best Route:\n", br)
    print("Elapsed time:\n", et)
