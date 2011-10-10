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
        return math.fabs(left-right)

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
        delta = calcDistance(newEnergy, energy)
        return math.exp(delta/temperature) if temperature > 0 else 1 # Is math.expm1 better for this?

def printStatus(status):
        print("=============== ", status["count"], " ===============")
        print("Current best energy: ", status["bestEnergy"], " from state: ", status["bestState"])
        print("last accepted energy: ", status["energy"], " from state: ", status["state"])
        print("current temperature: ", status["temperature"])

# initialState = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
initialState = [12, 2, 14, 0, 5, 13, 6, 8, 3, 10, 4, 11, 7, 9, 1]
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

best = annealer.run()

print(best)
