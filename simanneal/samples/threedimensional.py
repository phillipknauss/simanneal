import math

from samplebase import Sample

class ThreeDimensionalSample(Sample):
        """ Sample of using simulated annealing to optimize a two-dimensional data set """
        
        def __init__(self):
                self.reportPeriod = 500
                self.reportFunction = self.printStatus
                self.alpha = 0.6
                self.initialTemp = 1
                self.maxCount = 10000
                self.minEnergy = 0
                self.setInitialState( [(0,12,14), (1,2,13), (2,14,12), (3,0,11), (4,5,10), (5,13,9), (6,6,8), (7,8,7), (8,3,6), (9,10,5), (10,4,4), (11,11,3), (12,7,2), (13,9,1), (14,1,0)] )

        def calcDistance(self, left, right):
                """ Simple implementation of calculating the distance between two 2D points
                overrides implementation in parent class to work with 2D distances"""
                
                xDiff = right[0]-left[0]
                yDiff = right[1]-left[1]
                zDiff = right[2]-left[2]
                return math.sqrt((xDiff*xDiff)+(yDiff*yDiff)+(zDiff*zDiff))
