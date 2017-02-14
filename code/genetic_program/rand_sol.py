# from __future__ import print_function
import random
import numpy as np


def rand_sol(adj_mat, list_vert):
	to_visit = list_vert
	output_arr = [-1] * len(adj_mat)
	iteration_num = 0
	iteration_max = len(adj_mat)
	# continue until we've encountered all cycles/singletons
	while to_visit and iteration_num < iteration_max:	
		iteration_num += 1
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
			path = dfs(adj_mat, start)
			
			# reformat cycle and process adj_matrix and to_visit
			if path != None:
				# print 'cycle is ' + str(path)
				# print 'output array is ' + str(output_arr)
				# add path to the output_array
				for i in range(len(path)-1):
					if output_arr[path[i]] != -1:
						print adj_mat
						print path
						print 'ERROR: cycle overwritten!'
					output_arr[path[i]] = path[i+1]
				
				if path[0] != path[-1]:
					print 'ERROR: created a cycle that wasnt a cycle!'
					print path
				
				# remove cycle vertices from to_visit
				# and remove edges to those vertices
				for x in path[:-1]:
					# vertex removal in to_visit
					to_visit.remove(x)	
					# edge removal in adj_mat
					for i in range(len(adj_mat)):
						adj_mat[x][i] = 0
						adj_mat[i][x] = 0
				# print 'resulting matrix is ' + str(adj_mat)

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
	return output_arr

# call to dfs helper
def dfs(adj_mat, start):
	visited = [False] * len(adj_mat)
	return dfs_helper(adj_mat, start, visited, 1, start)


# recursive dfs helper method
def dfs_helper(adj_mat, current, visited, count, root):
	# print(visited, start, cnt, prev)

	# check if we have a cycle
	# if visited[current]:
	# 	return [current]
	if count != 1 and current == root:
		return [current]

	if visited[current]:
		return None

	# mark current vertex as visited
	visited[current] = True
	
	# if we exceed the cycle limit, we don't have a cycle
	if count > 5:
		return None
	
	# shuffle indices so we randomly pick the next node
	indices = np.array(range(len(adj_mat)))
	np.random.shuffle(indices)
	for i in indices:
		# check if an edge exists
		if adj_mat[current,i] == 1:
			n = dfs_helper(adj_mat, i, visited, count + 1, root)
			if n != None:
				# if we already found a loop, just return it
				if len(n) > 1 and n[0] == n[-1]:
					return n
				# otherwise add from the recursive call
				return [current] + n
	return None

#main test
def main():
	f = open('../phase1-processed/114.in','r')
	file = [[int(v) for v in line.split()] for line in f]
	list_vert = range(file[0][0])
	num_vert = file[0][0]
	
	adj_mat = np.zeros((num_vert, num_vert))
	for i in range(num_vert):
		for j in range(num_vert):
			adj_mat[i][j] = file[i+2][j]

	sol = rand_sol(adj_mat, list_vert)
	print sol
	num_connected = 0
	for i in sol:
		if i != -1:
			num_connected += 1
	print 'Kidneys connected: ' + str(num_connected)

if __name__ == '__main__':
	main()