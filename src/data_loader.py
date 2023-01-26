import numpy as np


class DataLoader:
    def __init__(self,  fileName, solFileName):
        self.fileName = fileName
        self.solFileName = solFileName

        self.loadHCPGraph()
        self.loadHCPRoute()

    def loadHCPGraph(self):
        '''
        Load adjency matrix from HCP file.
        '''
        f = open(self.fileName, 'r')
        self.graphName = f.readline().strip().split(maxsplit=2)[2]
        self.graphComment = f.readline().strip().split(maxsplit=2)[2]
        self.graphType = f.readline().strip().split(maxsplit=2)[2]
        self.graphDim = f.readline().strip().split(maxsplit=2)[2]
        self.graphDim = int(self.graphDim)

        if self.graphType == "HCP":
            self.adjencyMatrix = np.full((self.graphDim, self.graphDim), 2)
            self.format = f.readline().strip().split(maxsplit=2)[2]
            _ = f.readline()
            line = f.readline().strip()
            while line != "-1":
                x, y = line.split()
                x, y = int(x), int(y)
                self.adjencyMatrix[x - 1][y - 1] = 1
                self.adjencyMatrix[y - 1][x - 1] = 1
                line = f.readline().strip()

        for i in range(self.graphDim):
            self.adjencyMatrix[i][i] = 0

        f.close()

    def loadHCPRoute(self):
        '''
        Load route from HCP solution file.
        '''
        f = open(self.solFileName, 'r')

        self.routeName = f.readline()
        self.routeComment = f.readline()
        self.routeType = f.readline()
        self.routeDim = f.readline()
        _ = f.readline()

        line = f.readline().strip()
        self.route = []
        while line != "-1":
            self.route.append(int(line) - 1)
            line = f.readline().strip()

        f.close()

    def getAdjencyMatrix(self):
        '''
        Return loaded adjency matrix.
        '''
        return self.adjencyMatrix

    def getRoute(self):
        '''
        Return loaded route.
        '''
        return self.route

    def getDim(self):
        '''
        Return loaded graph dimension.
        '''
        return self.graphDim
