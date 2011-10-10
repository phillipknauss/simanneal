import unittest
import copy
import math

from simanneal.samples.twodimensional import TwoDimensionalSample

class TwoDimensionalSampleTest(unittest.TestCase):
    
    def setUp(self):
        self.sample = TwoDimensionalSample()

    """ neighbor is dependent on random calculations, and so isn't really testable as is """
    """ Todo: Factor random elements out of neighbor function allow it to be tested """
    # def test_neighbor(self): pass

    def test_calcDistance(self):
        expected = 1.0
        actual = self.sample.calcDistance((1,1),(2,1))
        self.assertEqual(expected, actual)

    def test_calcDelta(self):
        expected = 1.0
        actual = self.sample.calcDelta(2.0,1.0)
        self.assertEqual(expected, actual)

    def test_E(self):
        expected = 5.0
        actual = self.sample.E( [(1,1),(2,1),(3,1),(4,1),(5,1),(6,1)] )
        self.assertEqual(expected, actual)

    def test_temp(self):
        expected = 0.4
        actual = self.sample.temp(1);
        self.assertEqual(expected, actual)

    def test_P(self):
        expected = 1.0
        actual = self.sample.P(1.0,1.0,1.0)
        self.assertEqual(expected, actual)

    """ printStatus is just an IO class, so not worth testing """
    # def test_printStatus(self): pass
        
if __name__ == '__main__':
    unittest.main()
