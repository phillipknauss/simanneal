import random
import math
import copy

from simanneal.Annealer import Annealer

def neighbor(state):
        neighbor = copy.deepcopy(state) # Don't mutate the injected state
        for n in neighbor:
                next1 = random.randint(0, len(state)-1)
                next2 = random.randint(0, len(state)-1)
                neighbor[next1], neighbor[next2] = neighbor[next2], neighbor[next1] # Pythonic swap
        return neighbor

def calcDistance(left, right):
        xDiff = right[0]-left[0]
        yDiff = right[1]-left[1]
        zDiff = right[2]-left[2]
        return math.sqrt((xDiff*xDiff)+(yDiff*yDiff)+(zDiff*zDiff))

def calcDelta(energy1, energy2):
    return math.fabs(energy2-energy1)

def E(state):
        total = 0
        for i in range(len(state)-1):
               total += calcDistance(state[i+1], state[i])
        return total

alpha = 0.6
initialTemp = 1
def temp(countPercent):
        return initialTemp - (countPercent * alpha)

def P(energy, newEnergy, temperature):
        delta = calcDelta(newEnergy, energy)
        return math.exp(delta/temperature) if temperature > 0 else 1 # Is math.expm1 better for this?

def printStatus(status):
        print("=============== ", status["count"], " ===============")
        print("Current best energy: ", status["bestEnergy"], " from state: ", status["bestState"])
        print("last accepted energy: ", status["energy"], " from state: ", status["state"])
        print("current temperature: ", status["temperature"])

initialState = [(0,12,14), (1,2,13), (2,14,12), (3,0,11), (4,5,10), (5,13,9), (6,6,8), (7,8,7), (8,3,6), (9,10,5), (10,4,4), (11,11,3), (12,7,2), (13,9,1), (14,1,0)]
initialEnergy = E(initialState)

annealer = Annealer(initialState = initialState,
                    maxCount = 10000,
                    minEnergy = 0,
                    neighborFunction = neighbor,
                    energyFunction = E,
                    temperatureFunction = temp,
                    acceptanceProbabilityFunction = P)

# This version has regular reporting
""" annealer = simanneal.Annealer(initialState = initialState,
                    maxCount = 10000,
                    minEnergy = 0,
                    neighborFunction = neighbor,
                    energyFunction = E,
                    temperatureFunction = temp,
                    acceptanceProbabilityFunction = P,
                    reportPeriod = 500,
                    reportFunction = printStatus) """
print("initial energy: ", E(initialState))
best = annealer.run()

print(best)
