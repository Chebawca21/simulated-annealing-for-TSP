import numpy as np

class SimulatedAnnealing:
    def __init__(self, K=2000000, t0=0.3, tMin=0.19, alpha=0.9999995, fileName="FHCPCS/graph1.hcp"):
        self.fileName = fileName
        self.t0 = t0
        self.t = self.t0
        self.K = K
        self.tMin = tMin
        self.alpha = alpha
    
        f = open(self.fileName, 'r')
        self.name = f.readline().strip().split(maxsplit=2)[2]
        self.comment = f.readline().strip().split(maxsplit=2)[2]
        self.type = f.readline().strip().split(maxsplit=2)[2]
        self.dim = f.readline().strip().split(maxsplit=2)[2]
        self.dim = int(self.dim)

        if self.type == "HCP":
            self.adjencyMatrix = np.full((self.dim, self.dim), 2)
            self.format = f.readline().strip().split(maxsplit=2)[2]
            _ = f.readline()
            line = f.readline().strip()
            while line != "-1":
                x, y = line.split()
                x, y = int(x), int(y)
                self.adjencyMatrix[x - 1][y - 1] = 1
                self.adjencyMatrix[y - 1][x - 1] = 1
                line = f.readline().strip()
        
        f.close()

        self.bestRoute = np.empty((self.dim, 1))
        self.bestScore = self.dim * 4

    def neighbour(self, s):
        copy = s.copy()
        i = np.random.randint(self.dim)
        j = np.random.randint(self.dim)
        copy[i], copy[j] = copy[j], copy[i]
        return copy

    def temperature(self):
        if self.t <= self.tMin:
            self.t = self.tMin
        else:
            self.t = self.t * self.alpha

    def evalute(self, s):
        score = 0
        for i in range(self.dim):
            score = score + self.adjencyMatrix[s[i]][s[(i+1) % self.dim]]
        return score

    def probability(self, s1, s2):
        if s2 <= s1:
            return 1
        else:
            return np.exp(-(s2 - s1)/self.t)
    
    def anneal(self):
        s = np.random.choice(self.dim, self.dim, replace=False)
        for k in range(self.K):
            if k % (self.K/100) == 0:
                print(self.evalute(s), self.t)

            newS = self.neighbour(s)
            # print(self.evalute(s), self.evalute(newS), self.t)
            self.temperature()
            if self.probability(self.evalute(s), self.evalute(newS)) >= np.random.rand():
                if self.evalute(s) < self.bestScore:
                    self.bestRoute = s.copy()
                    self.bestScore = self.evalute(self.bestRoute)
                    print(self.bestScore, self.t)
                s = newS.copy()
        
        return self.bestRoute, self.bestScore