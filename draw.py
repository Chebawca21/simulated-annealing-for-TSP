import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class Draw:
    def __init__(self, adjencyMatrix, nodeSize=300):
        G = nx.from_numpy_matrix(adjencyMatrix)
        self.pos = nx.spring_layout(G)
        self.nodeSize = nodeSize
        plt.ion()
        self.fig = plt.figure()

    def routeToMatrix(self, route):
        i = 0
        dim = len(route)
        adjencyMatrix = np.full((dim, dim), 0)
        for _ in range(dim):
            currNode = route[i]
            if(i + 1 >= dim):
                nextNode = route[0]
            else:
                nextNode = route[i + 1]
            i = i + 1
            adjencyMatrix[currNode][nextNode] = 1
            adjencyMatrix[nextNode][currNode] = 1
        
        return adjencyMatrix

    def draw(self, route):
        plt.clf()
        G = nx.from_numpy_matrix(self.routeToMatrix(route))
        nx.draw(G, pos=self.pos, node_size=self.nodeSize)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.show()
    
    def stop(self):
        plt.ioff()
    