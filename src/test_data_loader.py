import unittest
import numpy as np
from data_loader import DataLoader
import json


class TestDataLoader(unittest.TestCase):
    '''
    Test DataLoader class in loading information
    from HCP files.
    '''
    def test_get_adjency_matrix(self):
        '''
        Test loading adjency matrix from HCP file.
        '''
        file = open("conf/test.json")
        data = json.load(file)
        file.close()

        dl = DataLoader(data['fileName'], data['solFileName'])
        adjencyMatrix = dl.getAdjencyMatrix()
        expected = [[0, 1, 2, 1, 1, 2],
                    [1, 0, 1, 2, 2, 1],
                    [2, 1, 0, 1, 2, 1],
                    [1, 2, 1, 0, 1, 2],
                    [1, 2, 2, 1, 0, 1],
                    [2, 1, 1, 2, 1, 0]]
        expected = np.array(expected)
        self.assertTrue(np.allclose(adjencyMatrix, expected))

    def test_get_route(self):
        '''
        Test loading route from HCP file.
        '''
        file = open("conf/test.json")
        data = json.load(file)
        file.close()

        dl = DataLoader(data['fileName'], data['solFileName'])
        route = dl.getRoute()
        expected = [0, 1, 2, 5, 4, 3]
        expected = np.array(expected)
        self.assertTrue(np.allclose(route, expected))

    def test_graph_dim(self):
        '''
        Test loading graph dimension from HCP file.
        '''
        file = open("conf/test.json")
        data = json.load(file)
        file.close()

        dl = DataLoader(data['fileName'], data['solFileName'])
        dim = dl.getDim()
        self.assertEqual(dim, 6)


if __name__ == '__main__':
    unittest.main()
