import networkx as nx
inFileName = 'blacklist.txt'
graphDir = 'phase1-processed/'
outFileDir = 'phase1-cycles/'

def main():
	inFile = open(inFileName, 'r')
	instance = inFile.readline()
	while instance != None:
		instance = instance.split('\n')[0]
		print("Starting instance " + instance + ".")
		with open(outFileDir + instance + '.in', 'w') as outFile:
			graph = nx.DiGraph()
			graphFile = open(graphDir + instance + '.in', 'r')

			# read the number of vertices
			num_vertices = int(graphFile.readline().split()[0])

			# read the children
			children_str = graphFile.readline().split()
			# children = [int(k) for k in children_str]
			
			dirEdges = []
			# read the adjacency matrix
			for i in range(num_vertices):
				line = graphFile.readline().split()
				edges = [int(k) for k in line]
				for j in range(len(edges)):
					if edges[j] == 1:
						dirEdges.append((i,j))
			graph = nx.DiGraph(dirEdges)
			cycles = nx.simple_cycles(graph)
			for cycle in cycles:
				string = ''
				count = 0
				for i in range(len(cycle) - 1):
					string += '{0} -> '.format(cycle[i])
					count += 1
				if count >= 5:
					continue
				string += "{0}\n".format(cycle[-1])
				outFile.write(string)
		print("Done writing " + outFileDir + instance + '.in.')
		instance = inFile.readline()
	

if __name__ == '__main__':
	main()