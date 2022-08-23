import numpy as np
from draw import Draw

class SimulatedAnnealing:
    def __init__(self, K=200000, t0=0.3, tMin=0.16, alpha=0.999995, fileName="FHCPCS/graph1.hcp", draw=True):
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

        self.draw = draw
        self.d = Draw(self.adjencyMatrix, nodeSize=30)

    def inverse(self, s, i, j):
        copy = s.copy()
        a = max(i, j)
        b = min(i, j)
        diff = a - b + 1
        for k in range(diff):
            copy[b + k] = s[a - k]
        return copy
    
    def insert(self, s, i, j):
        copy = s.copy()
        a = max(i, j)
        b = min(i, j)
        diff = a - b + 1
        copy[b] = s[a]
        for k in range(1, diff):
            copy[b + k] = s[b + k - 1]
        return copy

    def swap(self, s, i, j):
        copy = s.copy()
        copy[i], copy[j] = copy[j], copy[i]
        return copy

    def neighbour(self, s):
        i = np.random.randint(self.dim)
        j = np.random.randint(self.dim)
        candidates = (self.inverse(s, i, j), self.insert(s, i, j), self.swap(s, i, j))
        copy = min(candidates, key=lambda x: self.evalute(x))
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
                if self.draw:
                    self.d.draw(s)

            newS = self.neighbour(s)
            # print(self.evalute(s), self.evalute(newS), self.t)
            self.temperature()
            if self.probability(self.evalute(s), self.evalute(newS)) >= np.random.rand():
                if self.evalute(s) < self.bestScore:
                    self.bestRoute = s.copy()
                    self.bestScore = self.evalute(self.bestRoute)
                    print(self.bestScore, self.t)
                s = newS.copy()
        

        if self.draw:
            self.d.stop()
            self.d.draw(self.bestRoute)
        return self.bestRoute, self.bestScore