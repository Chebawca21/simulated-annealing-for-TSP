import numpy as np

class LSBA:
    def __init__(self):
        self.fileName = "FHCPCS/graph1.hcp"
    
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
        self.L = self.initTemp(40, 0.4)
        self.M = 120
        self.K = 10000

    def initTemp(self, Lmax, p0):
        L = []
        s = np.random.choice(self.dim, self.dim, replace=False)
        i = 0
        while i < Lmax:
            newS = self.neighbour(s)
            evNewS = self.evalute(newS)
            evS = self.evalute(s)
            if evNewS < evS:
                s = newS.copy()
            L.append(-abs(evNewS - evS) / np.log(p0)+ 0.1)
            i += 1
        return L


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
        if self.t <= 0.16:
            self.t = 0.16
        else:
            self.t = self.t * 0.999995

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

    def nearestNeighbour(self):
        curr = np.random.randint(self.dim)
        a = []
        unvisited = [i for i in range(self.dim)]
        unvisited.remove(curr)
        a.append(curr)
        while unvisited:
            new = min(unvisited, key=lambda k: self.adjencyMatrix[k][curr])
            unvisited.remove(new)
            a.append(new)
            curr = new
        
        return np.array(a)

# s = nearestNeighbour()

# bestRoute = s.copy()
# bestScore = evalute(bestRoute)
# print(bestRoute)
# t = temp

    def anneal(self):
        s = np.random.choice(self.dim, self.dim, replace=False)
        for k in range(self.K):
            tMax = max(self.L)
            t = 0
            c = 0

            if k % 100 == 0:
                print(self.evalute(s), tMax)

            for m in range(self.M):
                newS = self.neighbour(s)
                if self.evalute(newS) <= self.evalute(s):
                    if self.evalute(s) < self.bestScore:
                        self.bestRoute = s.copy()
                        self.bestScore = self.evalute(self.bestRoute)
                        print(self.bestScore, tMax)
                    s = newS.copy()
                else:
                    r = np.random.rand()
                    if np.exp(-(self.evalute(newS) - self.evalute(s)) / tMax) > r:
                        t += (self.evalute(newS) - self.evalute(s)) / np.log(r)
                        c += 1
                        s = newS.copy()

            if c != 0:
                if(t == 0):
                    print(tMax, t, c)
                self.L.remove(tMax)
                self.L.append(t/c)

        return self.bestRoute, self.bestScore

# print(bestRoute)
# print(evalute(bestRoute))