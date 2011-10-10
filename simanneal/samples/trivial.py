import math

from samplebase import Sample

class TrivialSample(Sample):
        """ Sample of using simulated annealing to optimize a simple data set """
        
        def __init__(self):
                self.reportPeriod = 500
                self.reportFunction = self.printStatus
                self.alpha = 0.6
                self.initialTemp = 1
                self.maxCount = 10000
                self.minEnergy = 0
                self.setInitialState( [12, 2, 14, 0, 5, 13, 6, 8, 3, 10, 4, 11, 7, 9, 1] )

        
        # def calcDistance(self, left, right): pass # Implemented in parent class
                
