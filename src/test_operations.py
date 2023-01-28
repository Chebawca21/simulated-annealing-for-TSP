import unittest
import operations


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


if __name__ == '__main__':
    unittest.main()
