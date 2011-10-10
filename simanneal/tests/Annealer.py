import unittest
import copy
import math

from simanneal.Annealer import Annealer

class AnnealerTests(unittest.TestCase):
    """ This was meant to be core unit tests, but Annealer really just
    loops through a bunch of injected functions which contain the important
    units to test """

    def neighborTest(self, state):
        return state

    def Etest(self, state):
        return 1

    def TempTest(self, countPercent):
        return 0

    def PTest(self, energy, newEnergy, temperature):
        return 1   

    def setUp(self):
        self.initialState = [12, 2, 14, 0, 5, 13, 6, 8, 3, 10, 4, 11, 7, 9, 1]
        self.annealer = Annealer(initialState = self.initialState,
        maxCount = 10000,
        minEnergy = 0,
        neighborFunction = self.neighborTest,
        energyFunction = self.Etest,
        temperatureFunction = self.TempTest,
        acceptanceProbabilityFunction = self.PTest)

    """ Annealer.run is not really a unit, but an aggregate loop through units,
    so isn't approprate to unit test. """

    """ _updateCandidate is a wrapper around the injected acceptanceProbabilityFunction, so shouldn't be tested here """
    # def test_updateCandidate(self): pass

    # A unit test for a single if statement isn't really useful
    """ def test_updateBest(self):
        expected = self.Etest(self.initialState)

        self.annealer._updateBest(self.initialState, self.Etest(self.initialState))
        actual = self.annealer.bestEnergy

        self.assertEqual(expected, actual) """
        
if __name__ == '__main__':
    unittest.main()
