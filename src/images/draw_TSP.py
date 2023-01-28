'''
Draws 5 different graphs:
undirected,
with restricted degree,
directed,
sample graph from FHCP before and after filling.
'''

import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Drawing undirected graph
    G1 = nx.Graph()
    G1.add_edge("A", "B", weight=1, color='r')
    G1.add_edge("A", "C", weight=2, color='r')
    G1.add_edge("B", "C", weight=5, color='b')
    G1.add_edge("A", "D", weight=5, color='b')
    G1.add_edge("B", "D", weight=6, color='b')
    G1.add_edge("C", "D", weight=6, color='r')
    G1.add_edge("A", "E", weight=6, color='b')
    G1.add_edge("B", "E", weight=4, color='r')
    G1.add_edge("C", "E", weight=7, color='b')
    G1.add_edge("D", "E", weight=2, color='r')

    nx.utils.pairwise

    colors = nx.get_edge_attributes(G1, 'color').values()

    pos = nx.spring_layout(G1)
    nx.draw_networkx_nodes(G1, pos)
    nx.draw_networkx_edges(G1, pos, edge_color=colors, width=3)
    nx.draw_networkx_labels(G1, pos)

    edgeWeights = nx.get_edge_attributes(G1, "weight")
    nx.draw_networkx_edge_labels(G1, pos, edgeWeights)
    plt.show()

    # Drawing graph with restricted degree
    G2 = nx.Graph()
    G2.add_edge("A", "B", weight=1, color='r')
    G2.add_edge("A", "C", weight=2, color='r')
    G2.add_edge("A", "D", weight=5, color='b')
    G2.add_edge("C", "D", weight=6, color='r')
    G2.add_edge("A", "E", weight=6, color='b')
    G2.add_edge("B", "E", weight=4, color='r')
    G2.add_edge("D", "E", weight=2, color='r')
    nx.utils.pairwise

    colors = nx.get_edge_attributes(G2, 'color').values()

    nx.draw_networkx_nodes(G2, pos)
    nx.draw_networkx_edges(G2, pos, edge_color=colors, width=3)
    nx.draw_networkx_labels(G2, pos)

    edgeWeights = nx.get_edge_attributes(G2, "weight")
    nx.draw_networkx_edge_labels(G2, pos, edgeWeights)
    plt.show()

    # Drawing directed graph
    G3 = nx.MultiDiGraph()
    G3.add_edge("F", "G", color='b')
    G3.add_edge("G", "F", color='b')
    G3.add_edge("F", "H", color='r')
    G3.add_edge("H", "F", color='b')
    G3.add_edge("G", "H", color='b')
    G3.add_edge("H", "G", color='r')
    G3.add_edge("F", "I", color='b')
    G3.add_edge("I", "F", color='r')
    G3.add_edge("G", "I", color='r')
    G3.add_edge("I", "G", color='b')
    G3.add_edge("H", "I", color='b')
    G3.add_edge("I", "H", color='b')
    nx.utils.pairwise

    colors = nx.get_edge_attributes(G3, 'color').values()

    pos = nx.spring_layout(G3)
    nx.draw_networkx_nodes(G3, pos)
    nx.draw_networkx_edges(G3, pos, edge_color=colors, width=3, connectionstyle="arc3,rad=0.1", arrowsize=15)
    nx.draw_networkx_labels(G3, pos)
    plt.show()

    # Drawing sample graph from FHCP before filling
    G4 = nx.Graph()
    G4.add_edge("A", "B", weight=1, color='b')
    G4.add_edge("A", "C", weight=1, color='b')
    G4.add_edge("B", "D", weight=1, color='b')
    G4.add_edge("C", "D", weight=1, color='b')
    G4.add_edge("A", "E", weight=1, color='b')
    G4.add_edge("B", "E", weight=1, color='b')
    G4.add_edge("D", "E", weight=1, color='b')
    nx.utils.pairwise

    colors = nx.get_edge_attributes(G4, 'color').values()

    pos = nx.spring_layout(G4)
    nx.draw_networkx_nodes(G4, pos)
    nx.draw_networkx_edges(G4, pos, edge_color=colors, width=3)
    nx.draw_networkx_labels(G4, pos)

    edgeWeights = nx.get_edge_attributes(G4, "weight")
    nx.draw_networkx_edge_labels(G4, pos, edgeWeights)
    plt.show()

    # # Drawing sample graph from FHCP after filling
    G5 = nx.Graph()
    G5.add_edge("A", "B", weight=1, color='b')
    G5.add_edge("A", "C", weight=1, color='b')
    G5.add_edge("B", "C", weight=2, color='r')
    G5.add_edge("A", "D", weight=2, color='r')
    G5.add_edge("B", "D", weight=1, color='b')
    G5.add_edge("C", "D", weight=1, color='b')
    G5.add_edge("A", "E", weight=1, color='b')
    G5.add_edge("B", "E", weight=1, color='b')
    G5.add_edge("C", "E", weight=2, color='r')
    G5.add_edge("D", "E", weight=1, color='b')
    nx.utils.pairwise

    colors = nx.get_edge_attributes(G5, 'color').values()

    nx.draw_networkx_nodes(G5, pos)
    nx.draw_networkx_edges(G5, pos, edge_color=colors, width=3)
    nx.draw_networkx_labels(G5, pos)

    edgeWeights = nx.get_edge_attributes(G5, "weight")
    nx.draw_networkx_edge_labels(G5, pos, edgeWeights)
    plt.show()
