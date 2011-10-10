import random # Prefer including namespace in calls rather than importing into the current namespace

class Annealer:
        def __init__(self,
                     initialState=None,
                     maxCount=None,
                     minEnergy=None,
                     neighborFunction=None,
                     energyFunction=None,
                     temperatureFunction=None,
                     acceptanceProbabilityFunction=None,
                     reportPeriod=None,
                     reportFunction=None):

                # These are all input variables and are not modified by Annealer
                self.initialState = initialState
                self.maxCount = maxCount
                self.minEnergy = minEnergy
                self.neighborFunction = neighborFunction
                self.energyFunction = energyFunction
                self.temperatureFunction = temperatureFunction
                self.acceptanceProbabilityFunction = acceptanceProbabilityFunction
                self.reportPeriod = reportPeriod
                self.reportFunction = reportFunction
                
        def run(self):
                """ An implementation of the Simulated Annealing metaheuristic """
                try:
                        state = self.initialState
                        energy = self.energyFunction(state)
                        bestState = 0
                        bestEnergy = energy
                        count = 0
                        while count < self.maxCount and energy > self.minEnergy:
                                newState = self.neighborFunction(state)
                                newEnergy = self.energyFunction(newState)
                                newTemp = self.temperatureFunction(count/self.maxCount)
                                if self.acceptanceProbabilityFunction(energy, newEnergy, newTemp) > random.random():
                                        state = newState
                                        energy = newEnergy
                                
                                if newEnergy < bestEnergy:
                                        bestState = newState
                                        bestEnergy = newEnergy
                                count = count + 1

                                if self.reportPeriod != None and count%self.reportPeriod==0:
                                        status = self._makeStatusObject(count, bestEnergy, bestState, energy, state, newTemp)
                                        self.reportFunction(status)
                        return self._makeStatusObject(count, bestEnergy, bestState, energy, state, newTemp)       
                except AttributeError:
                        print("Missing attributes.")
                        
        def _makeStatusObject(self, count, bestEnergy, bestState, energy, state, newTemp):
                return  {
                        'count': count,
                        'bestEnergy': bestEnergy,
                        'bestState': bestState,
                        'energy': energy,
                        'state': state,
                        'temperature': newTemp
                        }                                
