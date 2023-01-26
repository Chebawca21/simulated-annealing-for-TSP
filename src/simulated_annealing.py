import numpy as np
from draw import Draw
import time
import operations


class SimulatedAnnealing:
    def __init__(self, adjencyMatrix, route, dim, K=200000, t0=0.3, tMin=0.16, alpha=0.999995, draw=True, print=True):
        self.adjencyMatrix = adjencyMatrix
        self.route = route
        self.dim = dim

        self.t0 = t0
        self.t = self.t0
        self.K = K
        self.tMin = tMin
        self.alpha = alpha

        self.draw = draw
        if self.draw:
            self.d = Draw(self.adjencyMatrix, self.route, nodeSize=30)
        # time.sleep(1)

        self.print = print

        self.bestRoute = np.empty((self.dim, 1))
        self.bestScore = self.dim * 4

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

    def temperature(self):
        '''
        Update temperature parameter
        '''
        if self.t <= self.tMin:
            self.t = self.tMin
        else:
            self.t = self.t * self.alpha

    def probability(self, s1, s2):
        '''
        Calculate probability for current state s1 and new state s2.
        '''
        if s2 <= s1:
            return 1
        else:
            return np.exp(-(s2 - s1)/self.t)

    def anneal(self):
        '''
        Main anneal function.\n
        Starting from random point with class parameters.\n
        Returns best route, distance of this route and elapsed time.
        '''
        st = time.time()
        s = np.random.choice(self.dim, self.dim, replace=False)
        for k in range(self.K):
            if k % (self.K/100) == 0 and self.print:
                print(self.evalute(s), self.t)

            newS = self.neighbour(s)
            # print(self.evalute(s), self.evalute(newS), self.t)
            self.temperature()
            if self.probability(self.evalute(s), self.evalute(newS)) >= np.random.rand():
                if self.evalute(s) < self.bestScore:
                    self.bestRoute = s.copy()
                    self.bestScore = self.evalute(self.bestRoute)
                    if self.print:
                        print("New Best: ", self.bestScore, self.t)
                    if self.draw:
                        self.d.draw(s)
                s = newS.copy()

        if self.draw:
            self.d.stop()
            self.d.draw(self.bestRoute)

        et = time.time()
        elapsed = et - st

        return self.bestRoute, self.bestScore, elapsed
