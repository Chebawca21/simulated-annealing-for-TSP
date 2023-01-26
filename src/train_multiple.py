from simulated_annealing import SimulatedAnnealing
from data_loader import DataLoader

if __name__ == '__main__':
    N = 5
    dls = []
    sas = []

    dls.append(DataLoader("data/FHCPCS/graph1.hcp", "data/FHCPCS_sols/graph1.hcp.tou"))
    dls.append(DataLoader("data/FHCPCS/graph2.hcp", "data/FHCPCS_sols/graph2.hcp.tou"))
    dls.append(DataLoader("data/FHCPCS/graph12.hcp", "data/FHCPCS_sols/graph12.hcp.tou"))
    dls.append(DataLoader("data/FHCPCS/graph33.hcp", "data/FHCPCS_sols/graph33.hcp.tou"))

    sas.append(SimulatedAnnealing(dls[0].getAdjencyMatrix(), dls[0].getRoute(), dls[0].getDim(), K=100000, t0=0.3, tMin=0.16, alpha=0.999995, draw=False, print=False))
    sas.append(SimulatedAnnealing(dls[1].getAdjencyMatrix(), dls[1].getRoute(), dls[1].getDim(), K=150000, t0=0.3, tMin=0.16, alpha=0.999995, draw=False, print=False))
    sas.append(SimulatedAnnealing(dls[2].getAdjencyMatrix(), dls[2].getRoute(), dls[2].getDim(), K=350000, t0=0.3, tMin=0.155, alpha=0.999996, draw=False, print=False))
    sas.append(SimulatedAnnealing(dls[3].getAdjencyMatrix(), dls[3].getRoute(), dls[3].getDim(), K=850000, t0=0.3, tMin=0.145, alpha=0.999998, draw=False, print=False))
    print("Liczba miast\t", "Najlepszy wynik\t", "Najgorszy wynik\t", "Średni wynik\t", "Średni czas")

    for sa in sas:
        bestScore = 1000
        worstScore = -1
        sumScore = 0
        sumTime = 0
        for i in range(N):
            _, bs, et = sa.anneal()
            if bestScore > bs:
                bestScore = bs
            if worstScore < bs:
                worstScore = bs
            sumScore += bs
            sumTime += et
        print(sa.dim, "\t", bestScore, "\t", worstScore, "\t", sumScore/N, "\t", sumTime/N)
