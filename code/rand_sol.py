# from __future__ import print_function
import random
import numpy as np

def rand_sol(adj_mat, list_vert, num_vert):
	#from adj_mat, choose a random vertex and dfs for a cycle
	#of length <=5
	eps = 0.1

	cycle_list = [] # list 
	to_visit = list_vert
	output_arr = [-1] * num_vert

	# continue until we've encountered all cycles/singletons
	while to_visit:	


		# pick a random starting vertex
		start = random.sample(list_vert, 1)[0]

		# check if edges point into our start vertex
		edge_into = False
		for i in range(len(adj_mat)):
			if adj_mat[i][start] == 1:
				edge_into = True
				break

		# check if edges point from our start vertex
		edge_from = False
		for i in range(len(adj_mat)):
			if adj_mat[start][i] == 1:
				edge_from = True
				break

		# if there is an edge into and an edge from,
		# it is possibly in the loop
		if edge_into and edge_from:

			# find cycle
			prev = None
			visited = [False] * num_vert
			path = dfs(adj_mat, start, visited, 0, start, prev)
			
			# reformat cycle and process adj_matrix and to_visit
			if path != None:

				# add path to the output_array
				for i in range(len(path)-1):
					output_arr[path[i]] = path[i+1]
				cycle_list.append(output_arr)
				
				# remove cycle vertices from to_visit
				# and remove edges to those vertices
				for x in path[:-1]:
					# vertex removal in to_visit
					to_visit.remove(x)	
					# edge removal in adj_mat
					for i in range(len(adj_mat)):
						adj_mat[x][i] = 0
						adj_mat[i][x] = 0

		# if there is either no edges into or from,
		# then it cannot possibly be in a loop
		else:
			# if we had edges into, remove these edges
			if edge_into:
				for i in range(len(adj_mat)):
					adj_mat[i,start] = 0
			# if we had edges from, remove these edges
			elif edge_from:
				for i in range(len(adj_mat)):
					adj_mat[start,i] = 0
			to_visit.remove(start)
	return cycle_list

#dfs
def dfs(adj_mat, start, visited, cnt, root, prev):
	# print(visited, start, cnt, prev)
	if visited[start] and start == root:
		return [root]

	visited[start] = True
	
	if cnt == 5:
		if start == root:
			return [start]
		else:
			return None
	
	for i in range(len(adj_mat)):
		if adj_mat[start][i] == 1:
			n = dfs(adj_mat, i, visited, cnt + 1, root, start)
			if n != None:
				return [start] + n
			else:
				return None

#main test
def main():
	f = open('./phase1-processed/109.in','r')
	file = [[int(v) for v in line.split()] for line in f]
	list_vert = range(file[0][0])
	num_vert = file[0][0]
	
	#put into adj_mat... there's probably a better way hah
	adj_mat = np.zeros((num_vert, num_vert))
	for i in range(num_vert):
		for j in range(num_vert):
			adj_mat[i][j] = file[i+2][j]
	print rand_sol(adj_mat, list_vert, num_vert)

main()