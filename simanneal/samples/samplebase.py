import math
import copy
import random

from simanneal.Annealer import Annealer

class Sample(object):
        """ Base class for simulated annealing samples """
        """ Child methods should override these methods as appropriate to their needs """

        def run(self):
                """ Runs the annealing process """
                
                annealer = Annealer(initialState = self.initialState,
                    maxCount = self.maxCount,
                    minEnergy = self.minEnergy,
                    neighborFunction = self.neighbor,
                    energyFunction = self.E,
                    temperatureFunction = self.temp,
                    acceptanceProbabilityFunction = self.P,
                    reportPeriod = self.reportPeriod,
                    reportFunction = self.reportFunction)

                return annealer.run()

        def setInitialState(self, state):
                """ Setter for the initial state """
                """ Anticipate needing this for adding lazy loading and support for data sets too large to hold in memory """
                
                self.initialState = state
                
        def neighbor(self, state):
                """ In this sample, new candidates (neighbor states) are constructed by
                stepping through the previous state and swapping random elements"""
                
                neighbor = copy.deepcopy(state) # Don't mutate the injected state
                for n in neighbor:
                        next1 = random.randint(0, len(state)-1)
                        next2 = random.randint(0, len(state)-1)
                        neighbor[next1], neighbor[next2] = neighbor[next2], neighbor[next1] # Pythonic swap
                return neighbor

        def calcDelta(self, energy1, energy2):
                """ Determine the effective distance between two energy values """
                
                return math.fabs(energy2-energy1)

        def E(self, state):
                """ Energy (goal) function to optimize.
                For this implementation, we determine the energy by determining the sum of the distances between each node """
                
                total = 0
                for i in range(len(state)-1):
                        total += self.calcDistance(state[i+1], state[i])
                return total

        def temp(self, countPercent):
                """ Determine the temperature based on number of iterations """
                
                return self.initialTemp - (countPercent * self.alpha)

        def P(self, energy, newEnergy, temperature):
                """ Calculate the probability of switching to the new state """
                """ This is the decision-rule, adapted from Nascimento, et al., 2009 (See references) """
                
                delta = self.calcDelta(newEnergy, energy)
                return math.exp(delta/temperature) if temperature > 0 else 1 # Is math.expm1 better for this?

        def calcDistance(self, left, right):
                """ Works for simple values (float, int, etc),
                should be overridden in child classes to work with state element type """

                return math.fabs(right-left)                
        
        def printStatus(self, status):
                """ Dump the status to the console in a somewhat pretty way """
                """ This probably breaks SOI """
                
                print("=============== ", status["count"], " ===============")
                print("Current best energy: ", status["bestEnergy"], " from state: ", status["bestState"])
                print("last accepted energy: ", status["energy"], " from state: ", status["state"])
                print("current temperature: ", status["temperature"])
