import unittest
import numpy as np
import json
from data_loader import DataLoader
import operations
from draw import Draw
from simulated_annealing import SimulatedAnnealing


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


class TestOperations(unittest.TestCase):
    '''
    Test different operations for modifying solution
    to traveling salesman problem.
    '''
    def test_swap(self):
        '''
        Test swap operation.
        '''
        s = [0, 1, 2, 3, 4, 5]
        i = 2
        j = 5
        self.assertEqual(operations.swap(s, i, j), [0, 1, 5, 3, 4, 2])

    def test_insert(self):
        '''
        Test insert operation.
        '''
        s = [0, 1, 2, 3, 4, 5]
        i = 2
        j = 5
        self.assertEqual(operations.insert(s, i, j), [0, 1, 5, 2, 3, 4])

    def test_inverse(self):
        '''
        Test inverse operation.
        '''
        s = [0, 1, 2, 3, 4, 5]
        i = 2
        j = 5
        self.assertEqual(operations.inverse(s, i, j), [0, 1, 5, 4, 3, 2])


class TestDraw(unittest.TestCase):
    '''
    Test Draw class functions.
    '''
    def test_route_to_matrix(self):
        '''
        Test route to matrix transformation.
        '''
        file = open("conf/test.json")
        data = json.load(file)
        file.close()

        dl = DataLoader(data['fileName'], data['solFileName'])
        adjencyMatrix = dl.getAdjencyMatrix()
        route = dl.getRoute()

        draw = Draw(adjencyMatrix, route)
        matrixFromRoute = draw.routeToMatrix(route)
        expected = [[0, 1, 0, 1, 0, 0],
                    [1, 0, 1, 0, 0, 0],
                    [0, 1, 0, 0, 0, 1],
                    [1, 0, 0, 0, 1, 0],
                    [0, 0, 0, 1, 0, 1],
                    [0, 0, 1, 0, 1, 0]]
        expected = np.array(expected)
        self.assertTrue(np.allclose(matrixFromRoute, expected))


class TestSA(unittest.TestCase):
    '''
    Test SimulatedAnnealing functions.
    '''
    def test_evalute(self):
        '''
        Test calculatind distance of the solution.
        '''
        file = open("conf/test.json")
        data = json.load(file)
        file.close()

        dl = DataLoader(data['fileName'], data['solFileName'])
        adjencyMatrix = dl.getAdjencyMatrix()
        route = dl.getRoute()
        dim = dl.getDim()

        sa = SimulatedAnnealing(adjencyMatrix, route, dim)
        self.assertEqual(sa.evalute(route), 6)

    def test_temperature(self):
        '''
        Test calculating new temperature value.
        '''
        file = open("conf/test.json")
        data = json.load(file)
        file.close()

        dl = DataLoader(data['fileName'], data['solFileName'])
        adjencyMatrix = dl.getAdjencyMatrix()
        route = dl.getRoute()
        dim = dl.getDim()

        sa = SimulatedAnnealing(adjencyMatrix, route, dim, t0=0.5, tMin=0.2, alpha=0.5)
        sa.temperature()
        self.assertAlmostEqual(sa.t, 0.25)
        sa.temperature()
        sa.temperature()
        self.assertAlmostEqual(sa.t, 0.2)


if __name__ == '__main__':
    unittest.main()
