import random
import math
import copy

from simanneal.Annealer import Annealer

class TwoDimensionalSample(object):
        def __init__(self):
                self.reportPeriod = 500
                self.reportFunction = self.printStatus
                self.alpha = 0.6
                self.initialTemp = 1
                self.initialState = [(0,12), (1,2), (2,14), (3,0), (4,5), (5,13), (6,6), (7,8), (8,3), (9,10), (10,4), (11,11), (12,7), (13,9), (14,1)]
                
        def neighbor(self, state):
                neighbor = copy.deepcopy(state) # Don't mutate the injected state
                for n in neighbor:
                        next1 = random.randint(0, len(state)-1)
                        next2 = random.randint(0, len(state)-1)
                        neighbor[next1], neighbor[next2] = neighbor[next2], neighbor[next1] # Pythonic swap
                return neighbor

        def calcDistance(self, left, right):
                xDiff = right[0]-left[0]
                yDiff = right[1]-left[1]
                return math.sqrt((xDiff*xDiff)+(yDiff*yDiff))

        def calcDelta(self, energy1, energy2):
                return math.fabs(energy2-energy1)

        def E(self, state):
                total = 0
                for i in range(len(state)-1):
                        total += self.calcDistance(state[i+1], state[i])
                return total

        def temp(self, countPercent):
                return self.initialTemp - (countPercent * self.alpha)

        def P(self, energy, newEnergy, temperature):
                delta = self.calcDelta(newEnergy, energy)
                return math.exp(delta/temperature) if temperature > 0 else 1 # Is math.expm1 better for this?

        def printStatus(self, status):
                print("=============== ", status["count"], " ===============")
                print("Current best energy: ", status["bestEnergy"], " from state: ", status["bestState"])
                print("last accepted energy: ", status["energy"], " from state: ", status["state"])
                print("current temperature: ", status["temperature"])

        def run(self):                
                annealer = Annealer(initialState = self.initialState,
                    maxCount = 10000,
                    minEnergy = 0,
                    neighborFunction = self.neighbor,
                    energyFunction = self.E,
                    temperatureFunction = self.temp,
                    acceptanceProbabilityFunction = self.P,
                    reportPeriod = self.reportPeriod,
                    reportFunction = self.reportFunction)

                return annealer.run()
