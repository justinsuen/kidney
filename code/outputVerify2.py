import numpy as np
import os.path
solsFileName = 'solutions.out'
inputDir = 'phase1-processed/'

def main():
	solsFile = open(solsFileName, 'r')
	for instance in range(1,493):
		solution = solsFile.readline()
		solution = parse_solution(solution)

		inputFile = inputDir + str(instance) + '.in'
		children, graph = read_graph(inputFile)

		seen = set()
		score = 0
		for cycle in solution:
			if not verifyCycles(cycle, graph):
				print("{0}: Invalid solution -- invalid cycle.".format(instance))
				continue
			for vertex in cycle:
				if vertex in seen:
					print("{0}: Invalid solution -- duplicate vertices.".format(instance))
					continue
				seen.add(vertex)
				score += 1
				if vertex in children:
					score += 1
		# if score != solutionScore:
		# 	print("{0}: Invalid solution -- score doesn't match up with cycles.".format(instance))
		else:
			print("{0}: Valid solution. Score = {1}.".format(instance, score))


# Verifies that the cycles found are actual cycles by checking the edges with the adjacency matrix.
def verifyCycles(cycle, graph):
	if len(cycle) == 0:
		return True
	prev = cycle[0]
	next = cycle[-1]
	# Check edge from ending vertex to starting vertex
	if graph[next][prev] != 1:
			print(cycle)
			return False
	next = cycle[1]
	# Check edge from prev vertex to next vertex
	for i in range(1, len(cycle) - 1):
		if graph[prev][next] != 1:
			print(cycle)
			return False
		prev = cycle[i]
		next = cycle[i+1]
	return True

def read_graph(filename):
	# open the file
	file = open(filename, 'r')

	# read the number of vertices
	num_vertices = int(file.readline().split()[0])

	# read the children
	children_str = file.readline().split()
	children = [int(k) for k in children_str]

	# read the adjacency matrix
	mat = []
	for i in range(num_vertices):
		line = file.readline().split()
		mat.append([int(k) for k in line])

	return children, np.array(mat)

# Input: string in the specified output format
# Output: list of tuples
def parse_solution(solutionLine):
	if 'None' in solutionLine:
		return []
	cycles = solutionLine.split(";")
	solution = []
	for cycle in cycles:
		cycle = cycle.strip(' \n').split(' ')
		newCycle = []
		for i in range(len(cycle)):
			newCycle.append(int(cycle[i]))
		cycle = tuple(newCycle)
		solution.append(cycle)
	return solution


if __name__ == '__main__':
	main()