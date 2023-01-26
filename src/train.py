from simulated_annealing import SimulatedAnnealing
from data_loader import DataLoader

if __name__ == '__main__':
    dl = DataLoader("data/FHCPCS/graph1.hcp", "data/FHCPCS_sols/graph1.hcp.tou")
    sa = SimulatedAnnealing(dl.getAdjencyMatrix(), dl.getRoute(), dl.getDim(), K=100000, t0=0.3, tMin=0.16, alpha=0.999995, draw=False, print=True)
    br, bs, et = sa.anneal()
    print("Finished")
    print("Best Score: ", bs)
    print("Best Route:\n", br)
    print("Elapsed time:\n", et)
