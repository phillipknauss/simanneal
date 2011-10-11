""" A sample application to minimize the distance between two-dimensional points """

import math

from samplebase import Sample

class TwoDimensionalSample(Sample):
        """ Sample of using simulated annealing to optimize a two-dimensional data set """
        
        def __init__(self):
                self.reportPeriod = 500
                self.reportFunction = self.printStatus
                self.alpha = 0.6
                self.initialTemp = 1
                self.maxCount = 10000
                self.minEnergy = 0

        def calcDistance(self, left, right):
                """ Simple implementation of calculating the distance between two 2D points
                overrides implementation in parent class to work with 2D distances.
                This is the function we wish to minimize.
                Energy of a state is determined by iteratively applying this function to the candidate state."""
                
                xDiff = right[0]-left[0]
                yDiff = right[1]-left[1]
                return math.sqrt((xDiff*xDiff)+(yDiff*yDiff))

        
