from simulated_annealing import SimulatedAnnealing
from data_loader import DataLoader

if __name__ == '__main__':
    dl = DataLoader("data/FHCPCS/graph32.hcp", "data/FHCPCS_sols/graph32.hcp.tou")
    sa = SimulatedAnnealing(dl.getAdjencyMatrix(), dl.getRoute(), dl.getDim(), K=1400000, t0=0.3, tMin=0.135, alpha=0.9999985, draw=False, print=True)
    br, bs, et = sa.anneal()
    print("Finished")
    print("Best Score: ", bs)
    print("Best Route:\n", br)
    print("Elapsed time:\n", et)
