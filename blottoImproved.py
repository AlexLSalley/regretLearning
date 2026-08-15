import numpy as np
import random
import math

NUM_OF_BATTLES = 4
NUM_OF_SOLDIERS = 10

class Player:
	@staticmethod
	def generatePossibilities(numRemaining, currField, totalFields ):
		if totalFields - 1 == currField:
			return [str(numRemaining)]

		output = []
		for i in range(numRemaining + 1):
			# here we allocate i soldiers to current battlefield
			currOutputs = Player.generatePossibilities( numRemaining - i, currField + 1, totalFields)
			currOutputs = [ str(i)+","+item for item in currOutputs]
			output = output + currOutputs
		return output
	
	@staticmethod
	def calculateUtility(yourAction, opponentAction):
		yourUtility = 0
		for field in range(len(yourAction)):
			if yourAction[field] > opponentAction[field]:
				yourUtility += 1
			elif yourAction[field] < opponentAction[field]:
				yourUtility -= 1
		return yourUtility


	def __init__(self, soldierNum, battleNum):
		totalStrategies = math.comb( soldierNum + battleNum-1, battleNum-1 )
		
		self.strategies = Player.generatePossibilities(soldierNum, 0, battleNum)
		self.strategies = [ [int(item) for item in currStr.split(",")] for currStr in self.strategies]
		self.likelihoods = [1/totalStrategies] * totalStrategies

	def selectStrategy(self):
		num = random.random()
		for i in range(len(self.likelihoods)):
			if i == 0:
				if num < self.likelihoods[0]:
					return 0
			else:
				#print(sum(self.likelihoods[:i]))
				if num < sum(self.likelihoods[:i+1]) and num >= sum(self.likelihoods[:i]):
					return i
		return -1

	def play(self):
		return self.strategies[self.selectStrategy()]

	def calculateRegrets(self, chosenAction, opponentAction):
		regrets = [0] * len(self.strategies)

		chosenUtility = Player.calculateUtility(chosenAction, opponentAction)
		
		for i in range(len(self.strategies)):
			regrets[i] = Player.calculateUtility(self.strategies[i], opponentAction) - chosenUtility
		return regrets

	def updateLikelihoods(self, totalRegrets):
		normalizingFactor = np.sum(totalRegrets[totalRegrets > 0])

		if normalizingFactor == 0:
			self.likelihoods[i] = [1/len(self.likelihoods)] * len(self.likelihoods)
			return
		for i in range(len(self.strategies)):
			if totalRegrets[i] > 0:
				self.likelihoods[i] = totalRegrets[i]/normalizingFactor
			else:
				self.likelihoods[i] = 0

p1 = Player(5, 3)
p2 = Player(5, 3)

for trainingIteration in range(100):
	p1regrets = []
	p2regrets = []
	for gameRun in range(50):
		p1action = p1.play()
		if trainingIteration == 0 or trainingIteration == 99:
			print(str(trainingIteration)+": " +str(p1action))
		p2action = p2.play()
		if gameRun == 0:
			p1regrets = np.array(p1.calculateRegrets(p1action, p2action))
			p2regrets = np.array(p2.calculateRegrets(p2action, p1action))
		else:
			p1regrets = p1regrets + np.array(p1.calculateRegrets(p1action, p2action))
			p2regrets = p2regrets + np.array(p2.calculateRegrets(p2action, p1action))
	if trainingIteration == 99:
		merge = [(b, round(a*100,2)) for a,b in zip(p1.likelihoods, p1.strategies)]
		print(*merge, sep="\n")
	p1.updateLikelihoods(p1regrets)
	p2.updateLikelihoods(p2regrets)
