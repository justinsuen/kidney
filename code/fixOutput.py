import os.path
solsDir = 'phase2-sols/'
outFileName = 'solutions.out'
blackFileName = 'blacklist.txt'
geneticSolsFile = 'best_sols.out'


def main():
	blackFile = open(blackFileName, 'r')
	genFile = open(geneticSolsFile, 'r')
	with open(outFileName, 'w') as outFile:
		for i in range(1,493):
			fileName = solsDir + '{0}.out'.format(i)

			# If one of dp's solutions
			if os.path.isfile(fileName):
				file = open(fileName, 'r')
				score = int(file.readline())
				if score == 0:
					outFile.write('None\n')
					continue
				solution = file.readline()[1:-1]
				solution = parse_solution(solution)
				line = fixLine(solution)
				outFile.write(line)
				print('GENE: Finished writing instance {0}.'.format(i))
			# If one of genetic's solutions
			else:
				instance = int(blackFile.readline().strip('\n'))
				if instance != i:
					print("BIG ERROR - {0}".format(i))
				solution = genFile.readline()
				if solution == '\n':
					solution = "None\n"
				outFile.write(solution)
				print('RYAN: Finished writing instance {0}.'.format(i))

	genFile.close()
	blackFile.close()

# Input: list of tuples
# Output: string in the correct output format
def fixLine(solution):
	line = ''
	for cycle in solution:
		for j in range(len(cycle) - 1):
			line += '{0} '.format(cycle[j])
		line += '{0}; '.format(cycle[-1])
	line = line[:-2] + '\n'
	return line

# Parses the string of a list of tuples containing the solution.
# Returns a list of tuples of the same data.
def parse_solution(solutionLine):
	solutionLine = solutionLine[1:-1]
	solutionLine = solutionLine.replace("(", "")
	solutionLine = solutionLine.replace(",", "")
	cycles = solutionLine.split(")")
	solution = []
	for temp in cycles:
		cycle = temp.split(' ')
		newCycle = []
		for i in range(len(cycle)):
			if cycle[i] == '':
				continue
			newCycle.append(int(cycle[i]))
		cycle = tuple(newCycle)
		solution.append(cycle)
	return solution

if __name__ == '__main__':
	main()