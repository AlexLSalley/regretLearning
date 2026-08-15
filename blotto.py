import numpy as np
import random

NUM_OF_BATTLES = 4
NUM_OF_SOLDIERS = 10

class Player:
	def __init__(self, soldierNum, battleNum):
		self.strategy = [1/battleNum] * battleNum
		self.soldierNum = soldierNum
	
	def play(self):
		battleArray = np.zeros(len(self.strategy))

		for i in range(self.soldierNum):
			battleArray[self.selectBattlefield()] += 1
		return battleArray

	def selectBattlefield(self):
		num = random.random()
		for i in range(len(self.strategy)):
			if i == 0:
				if num < self.strategy[0]:
					return 0
			else:
				print(sum(self.strategy[:i]))
				if num < sum(self.strategy[:i+1]) and num >= sum(self.strategy[:i]):
					return i
		return -1

players = [Player(NUM_OF_SOLDIERS, NUM_OF_BATTLES), Player(NUM_OF_SOLDIERS, NUM_OF_BATTLES)]
numRounds = 10
print(*players)
for i in range(numRounds):
	array1 = players[0].play()
	array2 = players[1].play()

	results = np.zeros(len(array1))

	for j in range(len(array1)):
		if array1[j] > array2[j]:
			results[j] = 1
		if array1[j]== array2[j]:
			results[j] = 0
		if array1[j] < array2[j]:
			results[j] = -1
	print(array1)
	print(results)
