import numpy as np
import networkx as nx
from sklearn.manifold import MDS
import matplotlib.pyplot as plt


class Draw:
    '''
    Class to draw two figures.\n
    First one is the optimal route.
    Second is drawn with draw() function and can be updated during the
    execution of the program. After all the updates stop interactive mode
    with stop() function.
    '''
    def __init__(self, adjencyMatrix, route, nodeSize=300):
        '''
        Initialize Draw class. \n
            Parameters:
                adjencyMatrix: two dimensional array containg distances between nodes
                route: one dimensional array containg order in which nodes should be visited
                nodeSize (int): nodeSize for nx.draw() function

        Takes adjency matrix to establish node positions, route to draw the
        optimal route and node size (it needs to be smaller the more nodes
        graph has).
        '''
        self.nodeSize = nodeSize

        # Transforming adjency matrix to coordinates
        model = MDS(n_components=2, dissimilarity='precomputed', random_state=1)
        nodes = model.fit_transform(adjencyMatrix)
        G = nx.Graph()
        i = 0
        for node in nodes:
            G.add_node(i, pos=(node[0], node[1]))
            i += 1
        self.pos = nx.get_node_attributes(G, 'pos')

        # Plotting solution as a seperate figure
        plt.ion()
        self.fig = plt.figure()
        G = nx.from_numpy_matrix(self.routeToMatrix(route))
        nx.draw(G, pos=self.pos, node_size=self.nodeSize)
        plt.show()

        self.fig = plt.figure()

    def routeToMatrix(self, route):
        '''
        Transforms route into adjency matrix.
        '''
        i = 0
        dim = len(route)
        adjencyMatrix = np.full((dim, dim), 0)
        for _ in range(dim):
            currNode = route[i]
            if (i + 1 >= dim):
                nextNode = route[0]
            else:
                nextNode = route[i + 1]
            i = i + 1
            adjencyMatrix[currNode][nextNode] = 1
            adjencyMatrix[nextNode][currNode] = 1

        return adjencyMatrix

    def draw(self, route):
        '''
        Draw new route for the graph.
        '''
        plt.clf()
        G = nx.from_numpy_matrix(self.routeToMatrix(route))
        nx.draw(G, pos=self.pos, node_size=self.nodeSize)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.show()

    def stop(self):
        '''
        Stop pyplot interactive mode.
        '''
        plt.ioff()
