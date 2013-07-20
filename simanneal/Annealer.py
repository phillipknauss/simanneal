import random # Prefer including namespace in calls rather than importing into the current namespace

class annealer:
	""" An implementation of the Simulated Annealing metaheuristic """
	
	def __init__(self,
		     state=None,
		     maxCount=None,
		     minEnergy=None,
		     neighborFunction=None,
		     energyFunction=None,
		     temperatureFunction=None,
		     acceptanceProbabilityFunction=None,
		     reportPeriod=None,
		     reportFunction=None):

		# These are all input variables and are not modified by Annealer
		self.state = state
		self.maxCount = maxCount
		self.minEnergy = minEnergy
		self.neighborFunction = neighborFunction
		self.energyFunction = energyFunction
		self.temperatureFunction = temperatureFunction
		self.acceptanceProbabilityFunction = acceptanceProbabilityFunction
		self.reportPeriod = reportPeriod
		self.reportFunction = reportFunction

		# Encapsulate random values so we can unit test around them
		self.getRandom = lambda : random.random()
		
	def run(self):
		""" Main loop """
		
		self.energy = self.energyFunction(self.state)
		self.bestState = 0
		self.bestEnergy = self.energy
		newTemp = 0
		self.stop = None
		for count in range(1, self.maxCount+1):
			if self.energy <= self.minEnergy:
				break
			newState = self.neighborFunction(self.state)
			newEnergy = self.energyFunction(newState)
			newTemp = self.temperatureFunction(count)
			self._updateCandidate(self.energy, newEnergy, newTemp, newState)       
			self._updateBest(newState, newEnergy)

			self._report(count, newEnergy, newState, newTemp)

			if (self.stop is not None):
				self.stop = None
				break
				
		return self._createStatus(count, self.bestEnergy, self.bestState, newTemp)	 

	def _updateCandidate(self, currentEnergy, newEnergy, temperature, newState):
		""" Compares the acceptance probability to a random value and updates the candidate if necessary """
		
		if self.acceptanceProbabilityFunction(self.energy, newEnergy, temperature) > self.getRandom():
			self.state = newState
			self.energy = newEnergy

	def _updateBest(self, state, energy):
		""" Updates the tracking of the best state """
		
		if energy < self.bestEnergy:
			self.bestState = state
			self.bestEnergy = energy
	
	def _report(self, count, energy, state, temperature):
		""" Checks if we should report, then does so """
		
		if self.reportPeriod != None and count%self.reportPeriod==0:
			status = self._createStatus(count, energy, state, temperature)
			self.reportFunction(status)

	def _createStatus(self, count, energy, state, temperature):
		""" Convenience method for creating a status dictionary """
		
		return self._makeStatusObject(count, self.bestEnergy, self.bestState, energy, state, temperature)
	
	def _makeStatusObject(self, count, bestEnergy, bestState, energy, state, newTemp):
		""" Populates a dictionary with interesting information about process status """
		
		return	{
			'count': count,
			'bestEnergy': bestEnergy,
			'bestState': bestState,
			'energy': energy,
			'state': state,
			'temperature': newTemp
			}				 
