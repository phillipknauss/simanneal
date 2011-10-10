from simanneal.Annealer import Annealer

class Sample(object):
        """ Base class for simulated annealing samples """
        """ Todo: Move to its own module """
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
