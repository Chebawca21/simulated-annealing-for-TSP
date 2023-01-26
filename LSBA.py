import numpy as np
import operations


class LSBA:
    def __init__(self, adjencyMatrix, route, dim, K=200000, p0=0.4, Lmax=40, M=120, print=True):
        self.adjencyMatrix = adjencyMatrix
        self.route = route
        self.dim = dim

        self.M = M
        self.K = K
        self.p0 = p0
        self.Lmax = Lmax
        self.L = self.initTemp()

        self.print = print

        self.bestRoute = np.empty((self.dim, 1))
        self.bestScore = self.dim * 4

    def initTemp(self):
        '''
        Initialize temperature list.
        '''
        L = []
        s = np.random.choice(self.dim, self.dim, replace=False)
        i = 0
        while i < self.Lmax:
            newS = self.neighbour(s)
            evNewS = self.evalute(newS)
            evS = self.evalute(s)
            if evNewS < evS:
                s = newS.copy()
            L.append(-abs(evNewS - evS) / np.log(self.p0) + 0.1)
            i += 1
        return L

    def neighbour(self, s):
        '''
        Returns random neighbour from the neighbourhood of s.
        '''
        i = np.random.randint(self.dim)
        j = np.random.randint(self.dim)
        candidates = (operations.inverse(s, i, j), operations.insert(s, i, j), operations.swap(s, i, j))
        copy = min(candidates, key=lambda x: self.evalute(x))
        return copy

    def evalute(self, s):
        '''
        Returns distance of the solution s.
        '''
        score = 0
        for i in range(self.dim):
            score = score + self.adjencyMatrix[s[i]][s[(i+1) % self.dim]]
        return score

    def probability(self, s1, s2):
        '''
        Calculate probability for current state s1 and new state s2.
        '''
        if s2 <= s1:
            return 1
        else:
            return np.exp(-(s2 - s1)/self.t)

    def anneal(self):
        s = np.random.choice(self.dim, self.dim, replace=False)
        for k in range(self.K):
            tMax = max(self.L)
            t = 0
            c = 0

            if k % (self.K/100) == 0 and self.print:
                print(self.evalute(s), self.t)

            for m in range(self.M):
                newS = self.neighbour(s)
                if self.evalute(newS) <= self.evalute(s):
                    if self.evalute(s) < self.bestScore:
                        self.bestRoute = s.copy()
                        self.bestScore = self.evalute(self.bestRoute)
                        if self.print:
                            print("New Best: ", self.bestScore, self.t)
                    s = newS.copy()
                else:
                    r = np.random.rand()
                    if np.exp(-(self.evalute(newS) - self.evalute(s)) / tMax) > r:
                        t += (self.evalute(newS) - self.evalute(s)) / np.log(r)
                        c += 1
                        s = newS.copy()

            if c != 0:
                self.L.remove(tMax)
                self.L.append(t/c)

        return self.bestRoute, self.bestScore
