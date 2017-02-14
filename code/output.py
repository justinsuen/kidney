import os.path
import sys
import time
from collections import Counter
sys.setrecursionlimit(1000000)
graphDirectory = 'phase1-processed/'
cycleDirectory = 'phase1-cycles/'
solsDirectory = 'phase2-sols/'
children = []
answers = {}
vertexToCycle = {}
timeoutTime = 60
answersMaxSize = 1100000

def main():
	global children
	startTime = time.time()
	for instance in range(1,493):
		try:
			solsFile = solsDirectory + str(instance) + '.out'
			cycleFile = cycleDirectory + str(instance) + '.in'
			graphFile = graphDirectory + str(instance) + '.in'

			# Not an instance for which a cycle was found
			if not os.path.isfile(cycleFile):
				continue

			# Already have a solution for this instance
			if os.path.isfile(solsFile):
				continue

			print("Starting instance {0}.".format(instance))
			cycles = read_cycles(cycleFile)
			children = read_graph(graphFile)
			buildVertexToCycle(cycles)

			# solution = dynamic(cycles, startTime)
			solution = dynamicIter(cycles)
			answers.clear()
			vertexToCycle.clear()

			write_solution(solsFile, solution)
		
		# Catch instances which take too long.
		except TimeoutError:
			print('Instance {0} took longer than {1} mins.'.format(instance, timeoutTime))
			score, cycles = findMaxAnswer()
			print('Max score: {0}. Path: {1}.'.format(score, cycles))
			print('----------------------------------------------------------')
			continue
	endTime = time.time()
	print("Took {0} minutes.".format((endTime - startTime)/60))

# Finds the highest scoring answer found so far
def findMaxAnswer():
	currMax = -float('inf')
	currCycles = []
	for key in answers:
		score, cycles = answers[key]
		if score > currMax:
			currMax = score
			currCycles = cycles
	return currMax, currCycles


# Builds a dictionary which maps a vertex to all the cycles it is included in
def buildVertexToCycle(cycles):
	for cycle in cycles:
		for vertex in cycle:
			if vertex not in vertexToCycle:
				vertexToCycle[vertex] = [cycle]
			else:
				vertexToCycle[vertex].append(cycle)

# Assigns a score to a cycle based on vertices
def score(cycle):
	total = 0
	for member in cycle:
		total += 1
		if member in children:
			total += 1
	return total

# Recursive version of dp.
def dynamic(cycles, startTime):
	if time.time() - startTime >= 60 * timeoutTime:
		raise TimeoutError()
	if len(cycles) == 0:
		return 0, []
	elif len(cycles) == 1:
		cycle = cycles[0]
		return score(cycle), [cycle]
	else:
		cyclesHashable = frozenset(cycles)
		if cyclesHashable in answers:
			return answers[cyclesHashable]

		currEle = cycles[-1]
		exclude = set()
		for member in currEle:
			cyclesToExclude = vertexToCycle[member]
			for cycle in cyclesToExclude:
				exclude.add(cycle)

		newCycles = []
		for cycle in cycles:
			if cycle not in exclude:
				newCycles.append(cycle)

		scoreUsed, pathUsed = dynamic(newCycles, startTime)
		scoreUsed += score(currEle)
		scoreUnused, pathUnused = dynamic(cycles[:-1], startTime)
		answer = max(scoreUsed, scoreUnused)
		path = []
		if answer == scoreUsed:
			path = pathUsed + [currEle]
		else:
			path = pathUnused
		answers[cyclesHashable] = answer, path
		return answer, path

# Deletes the least recently used entries from answers
def cleanAnswers(counter, to_find):
	if len(answers) > answersMaxSize:
		least_common = counter.most_common()[:-to_find-1:-1]
		for cycle in least_common:
			del answers[cycle[0]]
		counter.clear()
		# print('Resized answers.')

# Iterative version. Currently using this one.
def dynamicIter(cycles):
	counter = Counter()
	stack = []
	stack.append(cycles)
	origCycles = frozenset(cycles)
	partitionSize = 10
	max_score = 0

	# Used to adjust # of entries being deleted if dp relies on too many past solutions.
	def adjustPartitionSize(max_score):
		nonlocal partitionSize
		currMax = findMaxAnswer()[0]
		if currMax <= max_score:
			partitionSize *= 10
			print(currMax)
			return currMax
		print(max_score)
		return max_score

	while len(stack) > 0:
		# Attempt to handle the memory issue.
		if partitionSize < answersMaxSize and len(answers) > answersMaxSize:
			adjustPartitionSize(max_score)
		cleanAnswers(counter, answersMaxSize//partitionSize)

		cycles = stack.pop()
		# Create hashable cycle for answers dictionary
		cyclesHashable = frozenset(cycles)
		if cyclesHashable in answers:
			continue

		if len(cycles) == 0:
			 answers[cyclesHashable] = 0, []
			 counter[cyclesHashable] += 1
			 continue
		elif len(cycles) == 1:
			cycle = cycles[0]
			answers[cyclesHashable] = score(cycle), [cycle]
			counter[cyclesHashable] += 1
			continue

		currEle = cycles[-1]
		exclude = set()
		for member in currEle:
			cyclesToExclude = vertexToCycle[member]
			for cycle in cyclesToExclude:
				exclude.add(cycle)

		newCycles = []
		for cycle in cycles:
			if cycle not in exclude:
				newCycles.append(cycle)

		usedCyclesHashable = frozenset(newCycles)
		unusedCyclesHashable = frozenset(cycles[:-1])
		if usedCyclesHashable not in answers or unusedCyclesHashable not in answers:
			stack.append(cycles)
			stack.append(newCycles)
			stack.append(cycles[:-1])
			continue

		scoreUsed, pathUsed = answers[usedCyclesHashable]
		counter[usedCyclesHashable] += 1
		scoreUsed += score(currEle)
		scoreUnused, pathUnused = answers[unusedCyclesHashable]
		counter[usedCyclesHashable] += 1
		answer = max(scoreUsed, scoreUnused)
		path = []
		if answer == scoreUsed:
			path = pathUsed + [currEle]
		else:
			path = pathUnused
		answers[cyclesHashable] = answer, path
		counter[cyclesHashable] += 1
	return answers[cyclesHashable]



def read_graph(filename):
	# open the file
	file = open(filename, 'r')

	# read the number of vertices
	num_vertices = int(file.readline().split()[0])

	# read the children
	children_str = file.readline().split()
	children = [int(k) for k in children_str]
	return children

# Cycles were written to file in the format of "x -> y -> z"
# Returns a list of tuples (cycles)
def read_cycles(filename):
	cycles = []
	file = open(filename, 'r')
	for line in file:
		if line == '': 
			break
		cycle = line.split(' -> ')
		for i in range(len(cycle)):
			cycle[i] = int(cycle[i])
		cycles.append(tuple(cycle))
	return cycles

def write_solution(filename, solution):
	with open(filename, 'w') as file:
		score = solution[0]
		file.write('{0}\n'.format(score))
		file.write(str(solution[1]))
	print("Done writing " + filename + ".")


if __name__ == '__main__':
	main()
