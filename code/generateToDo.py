import os.path

cycleDir = 'phase1-cycles/'
inputDir = 'phase1-processed/'
solsDir = 'phase2-sols/'
completedFileName = 'completed.txt'
todoFileName = 'todo.txt'
blacklistFileName = 'blacklist.txt'

def main():
	# Edge Cutoff #
	# cutoff = 2000050

	# completedFile = open(completedFileName, 'w')
	# todoFile = open(todoFileName, 'w')
	# toBeWritten = []
	# for i in range(1, 493):
	# 	cycleFile = cycleDir + '{0}.in'.format(i)
	# 	if os.path.isfile(cycleFile):
	# 		completedFile.write("{0}\n".format(i))
	# 	else:
	# 		toBeWritten += [i]

	# blacklistSet = set()
	# blacklistFile = open('blacklist.txt', 'r')
	# for line in blacklistFile:
	# 	blacklistSet.add(int(line))
	# 	fileName = cycleDir + str(int(line)) + '.in' 
	# 	if os.path.isfile(fileName):
	# 		os.remove(fileName)

	# edgeFile = open('numEdges.txt', 'r')
	# for inst in toBeWritten:
	# 	currInstEdge = edgeFile.readline().split(' - ')
	# 	while int(currInstEdge[0]) != inst:
	# 		currInstEdge = edgeFile.readline().split(' - ')
	# 	numEdges = int(currInstEdge[1])
	# 	if numEdges < cutoff and inst not in blacklistSet:
	# 		todoFile.write('{0}\n'.format(int(currInstEdge[0])))

	# completedFile.close()
	# todoFile.close()

	with open(blacklistFileName, 'w') as blacklistFile:
		for i in range(1,493):
			solsFile = solsDir + '{0}.out'.format(i)
			if not os.path.isfile(solsFile):
				blacklistFile.write('{0}\n'.format(i))



if __name__ == '__main__':
	main()