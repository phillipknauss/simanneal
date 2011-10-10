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
                self.setInitialState( [(0,12), (1,2), (2,14), (3,0), (4,5), (5,13), (6,6), (7,8), (8,3), (9,10), (10,4), (11,11), (12,7), (13,9), (14,1)] )

        def calcDistance(self, left, right):
                """ Simple implementation of calculating the distance between two 2D points
                overrides implementation in parent class to work with 2D distances"""
                
                xDiff = right[0]-left[0]
                yDiff = right[1]-left[1]
                return math.sqrt((xDiff*xDiff)+(yDiff*yDiff))

        
