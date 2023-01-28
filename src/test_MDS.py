'''
Test accuracy of the MDS algorithm on the graph specified in
conf/train.json file.
'''

from sklearn.manifold import MDS
from math import sqrt
from data_loader import DataLoader
import json


def distance(p1, p2):
    '''
    Calculate euclidean distance between p1 and p2.
    '''
    r = (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2
    return sqrt(r)


if __name__ == '__main__':
    file = open("conf/train.json")
    data = json.load(file)

    dl = DataLoader(data['fileName'], data['solFileName'])
    am = dl.getAdjencyMatrix()

    model = MDS(n_components=2, dissimilarity='precomputed', random_state=1)
    nodes = model.fit_transform(am)

    for j in range(66):
        max1 = 0
        min2 = 10
        for i in range(66):
            a = am[j][i]
            b = distance(nodes[j], nodes[i])
            if a == 1 and b > max1:
                max1 = b
            if a == 2 and b < min2:
                min2 = b
        print(max1, min2)
