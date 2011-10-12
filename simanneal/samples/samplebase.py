import math
import copy
import random
import sys

from simanneal.Annealer import Annealer

class Sample(object):
        """ Base class for simulated annealing samples """
        """ Child methods should override these methods as appropriate to their needs """

        def __init__(self):
                self.annealer = Annealer()

        def run(self):
                """ Runs the annealing process """
                
                self.annealer.state = self.state
                self.annealer.maxCount = self.maxCount
                self.annealer.minEnergy = self.minEnergy
                self.annealer.neighborFunction = self.neighbor
                self.annealer.energyFunction = self.E
                self.annealer.temperatureFunction = self.temp
                self.annealer.acceptanceProbabilityFunction = self.P
                self.annealer.reportPeriod = self.reportPeriod
                self.annealer.reportFunction = self.reportFunction

                return self.annealer.run()

        def stop(self):
                self.annealer.stop = True
        
        def setState(self, state):
                """ Setter for the initial state """
                """ Anticipate needing this for adding lazy loading and support for data sets too large to hold in memory """
                
                self.state = state
                
        def neighbor(self, state):
                """ In this sample, new candidates (neighbor states) are constructed by
                stepping through the previous state and swapping random elements"""
                
                neighbor = copy.deepcopy(state) # Don't mutate the injected state

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
                if state==0: # Invalid state has no energy
                        return 0
                for i in range(len(state)-1):
                        total += self.calcDistance(state[i+1], state[i])
                return total

        def temp(self, numIterations):
                """ Determine the temperature based on number of iterations """

                denom = numIterations*self.alpha
                
                return 1/denom if denom > 0 else 0

        def P(self, energy, newEnergy, temperature):
                """ Calculate the probability of switching to the new state """
                """ This is the decision-rule, adapted from Nascimento, et al., 2009 (See references) """
                
                delta = self.calcDelta(newEnergy, energy)

                minTemp = 0.00001 # use minimum to avoid div/0 and buffer overflow
                try:
                        return minTemp if temperature==0 else math.exp((round(delta,2)/round(temperature,2))) if temperature > minTemp else 1 # Is math.expm1 better for this?
                except OverflowError as detail:
                        print("Overflow:","delta=",round(delta,2),"temp=",round(temperature,2))
                        return minTemp
                

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
