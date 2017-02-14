import random
import numpy as np
from rand_sol import rand_sol
from multiprocessing import Pool
import gc

class GeneticProgram:

    """
    constructor
    @param  starting_solutions: randomly chosen solutions
            adjacency_matrix: adjacency matrix for directed edges
            children_vertices: list of vertex numbers 
    """
    def __init__(self, starting_solutions, adjacency_matrix, children_vertices):
        self.population = starting_solutions
        self.adj_matrix = adjacency_matrix
        self.children = set(children_vertices)
        self.num_vertices = adjacency_matrix.shape[0]


    """
    simulateNature: main call to run the genetic algorithm
    @param  num_generations: number of iterations we run the crossovers
            init_population: number of possible paths per generation
    @return favorite_child: "optimal" vertex set
    """
    def simulateNature(self, num_generations, keep_unfit_chance = .2, keep_parent_cutoff = 1, breed_parent_cutoff = 1):

        current_generation = self.population
        past_averages = []
        # crossover for num_generations
        for i in range(num_generations):
            if i > 4 and past_averages[-1] == past_averages[-2] and past_averages[-2] == past_averages[-3] \
                and past_averages[-3] == past_averages[-4]:
                break
            current_generation = self.createNextGeneration(current_generation, keep_unfit_chance, keep_parent_cutoff, breed_parent_cutoff)
            avg_fitness = self.calculateAvgFitness(current_generation)
            print 'Generation ' + str(i+1) + ' complete. Average fitness is ' \
             + str(avg_fitness)
            past_averages.append(avg_fitness)
        
        # find the best child and return it
        favorite_child = 0
        best_fitness = float("-inf")
        for i in range(len(current_generation)):
            cur_fit = self.calculateFitness(current_generation[i])
            if cur_fit > best_fitness:
                favorite_child = i
                best_fitness = cur_fit
        print("Best fitness is " + str(best_fitness))
        gc.collect()
        return current_generation[favorite_child]

    """
    createNextGeneration: simulates a new generation of paths
    @param  generation: the previous generation we are making a new one from
            keep_bad_chance: the percentage we keep a below average parent to mate
            mutate_rate: the chance a child has of mutating
            survival_rate: the percentage of members we want our next generation to be
    @return children: the new generation
    """
    def createNextGeneration(self, generation, keep_bad_chance, kcutoff, bcutoff, mutate_rate = 0.01):
        # This isn't that necessary since we have randomness in crossover.
        # Do it if we have extra time.
        MUTATIONS = False

        population = len(generation)
        avg = self.calculateAvgFitness(generation)
        fit = []
        children = []
        # filter parents
        for pSet in generation:
            pFitness = self.calculateFitness(pSet)
            # keep the exceptional parents as children
            if pFitness >= kcutoff * avg or random.randint(1, int(1/keep_bad_chance)) == 1:
                children.append(pSet)
                fit.append(pSet)
            # add above average parents to breed (or lucky ones)
            elif pFitness >= bcutoff * avg or random.randint(1, int(1/keep_bad_chance)) == 1:
                fit.append(pSet)
        
        # parallel compute
        pool = Pool()
        inputs = []
        for mate_pair in range(population - len(children)):
            inputs.append((self.num_vertices, self.adj_matrix, fit[mate_pair%len(fit)], random.choice(fit)))
        children += pool.imap_unordered(evolve, inputs)

        avg = self.calculateAvgFitness(children)
        return children

    """
    calculateFitness: Calculates the total distance of a solution.
    @param vertex_array: array of size n, which each value corresponds to its connection. 
    @return score: calculates num_children * 2 + num_adults
    """
    def calculateFitness(self, vertex_array):
        score = 0
        for v in vertex_array:
            if v != -1:
                # if it's connected, it gets a kidney
                score += 1
                if v in self.children:
                    # if it's a child, it gets an extra point
                    score += 1
        return score

    """
    calculateAvgFitness: find the average score of all the inhabitants
    @param generation: as described in createGeneration
    @return score: a float of the average distance
    """
    def calculateAvgFitness(self, generation):
        score = 0
        for vertex_array in generation:
            score += self.calculateFitness(vertex_array)
        return float(score)/len(generation)

"""
evolve: The hard part. Take two set of vertices and crossover by
        randomly picking valid cycles from the two parents.
@param sol1: father solution
       sol1: mother solution
@return child: crossover solution
"""
#def evolve(num_vertices, adj_matrix, sol1, sol2, sample_rate = 100):
def evolve(args, sample_rate = 1):
    num_vertices, adj_matrix, sol1, sol2 = args
    # make sure we don't change anything we still need
    vertices_left = set(range(num_vertices))
    child = -1 * np.ones(num_vertices).astype(int)

    # sample cycles from parents
    for _ in range(num_vertices * sample_rate):
        # if we have a perfect solution, then we stop!
        if len(vertices_left) == 0:
            break
        # randomly pick a parent to sample from
        if random.randint(0,1) == 0:
            sampler = sol1
        else:
            sampler = sol2
        # randomly pick a vertex to start a cycle from
        vertex = random.sample(vertices_left, 1)[0]
        # check if theres no cycle
        if sampler[vertex] == -1:
            continue
        cycleToAdd = findCycle(sampler, vertex)
        # if the cycle can be added to the child
        if set(cycleToAdd.keys()).issubset(vertices_left):
            # add the vertex
            for key, val in cycleToAdd.iteritems():
                child[int(key)] = int(val)
                vertices_left.remove(val)

    # TODO: IMPLEMENT GREEDY REPOPULATION OF CYCLES
    if len(vertices_left) > 1:
        adj_mat_copy = np.zeros((len(adj_matrix), len(adj_matrix))).astype(int)
        for i in vertices_left:
            for j in vertices_left:
                adj_mat_copy[i,j] = adj_matrix[i,j]
        extra_sols = rand_sol(adj_mat_copy, list(vertices_left))
        for i in range(len(extra_sols)):
            if extra_sols[i] != -1:
                if child[i] != -1:
                    print 'ERROR: random repopulation encountered overwrite!'
                child[i] = extra_sols[i]
    return child

"""
findCycle: takes a vertex array of size n and a starting point and find the cycle that vertex is in
@param  solution: vertex array of size n
        vertex: starting vertex
@return cycle: dictionary with key = vertices and val = vertices pointed to
"""
def findCycle(solution, vertex, max_cycle_len = 5):
    cycle = {}
    first = vertex
    # traverse the cycle (we assume they are cycles)
    for _ in range(max_cycle_len):
        next_vertex = solution[int(vertex)]
        cycle[int(vertex)] = int(next_vertex)
        if next_vertex == first:
            return cycle
        vertex = next_vertex
    print cycle
    print solution
    print 'ERROR: vertex ' + str(vertex) + ' is in a cycle of length greater than ' + str(max_cycle_len)

def read_in_file(filename):
    f = open(filename,'r')
    file = [[int(v) for v in line.split()] for line in f]
    f.close()
    list_vert = range(file[0][0])
    num_vert = file[0][0]
    children = file[1]
    
    adj_mat = np.zeros((num_vert, num_vert)).astype(int)
    for i in range(num_vert):
        for j in range(num_vert):
            adj_mat[i][j] = file[i+2][j]
    return adj_mat, children

def output_cycle_file(cycles_string_array):
    filename = './solution_456.out'
    with open(filename, 'w') as file:
        for c in cycles_string_array:      
            file.write(c)
    file.close()

def cycles_list_to_string(cycles_list):
    cycles_string = ""
    for cycle in cycles_list:
        for c in cycle:
            cycles_string += ' ' + str(c)
        cycles_string += ';'
    cycles_string = cycles_string[1:-1]
    return cycles_string + '\n'

def process_output_solution(solution):
    vertices_left = range(len(solution))
    cycles = []
    for i in range(len(solution)):
        if solution[i] in vertices_left and solution[i] != -1:
            cycle = []
            first = solution[i]
            vertex = first
            for _ in range(5):
                next_vertex = solution[vertex]
                cycle.append(vertex)
                if next_vertex == first:
                    cycles.append(cycle)
                    break
                vertices_left.remove(next_vertex)
                vertex = next_vertex
    return cycles


def run_on_instance(filename):
    POPULATION = 20
    GENERATIONS = 10
    KEEP_UNFIT_CHANCE = .1
    KEEP_PARENT_AVG = 1.1
    BREED_PARENT_AVG = 1

    adj_mat, children = read_in_file(filename)

    print 'Running genetic algorithm on ' + filename

    # create starting population
    print 'Initializing population...'
    starting_population = []
    pool = Pool()
    input_pool = []
    for _ in range(POPULATION):
        input_pool.append((adj_mat.copy(), range(len(adj_mat))))
        # individual = rand_sol(adj_mat.copy(), range(len(adj_mat)))
        # starting_population.append(individual)
    starting_population = list(pool.imap_unordered(rand_sol_helper, input_pool))
    
    print 'Population of size ' + str(POPULATION) + ' successfully birthed.'

    # run genetic algorithm
    GP = GeneticProgram(starting_population, adj_mat, children)
    solution = GP.simulateNature(GENERATIONS, KEEP_UNFIT_CHANCE, KEEP_PARENT_AVG, BREED_PARENT_AVG)
    return solution

def rand_sol_helper(args):
    return rand_sol(*args)

def read_blacklist(filename):
    with open(filename, 'r') as f:
        numbers = f.readlines()
    f.close()
    for i in range(len(numbers)):
        numbers[i].replace('\n', '')
        numbers[i] = int(numbers[i])
    numbers.sort()

    return numbers

def main():
    solution_array = []

    instances = read_blacklist('./blacklist-3.txt')
    print instances[272]
    for i in [456]:
        filename = '../phase1-processed/' + str(i) + '.in'
        solution = run_on_instance(filename)
        cycles_list = process_output_solution(solution)
        cycles_string = cycles_list_to_string(cycles_list)
        solution_array.append(cycles_string)
    output_cycle_file(solution_array)

if __name__ == '__main__':
    main()




    # """
    # mutate: Once in a while, mutate to avoid local maxima
    # @param  path: the path to mutate
    # @return mutant: the mutated path (two nodes swapped)
    # """
    # def mutate(self, path):
    #     # pick random path and random index
    #     numPaths = len(path)
    #     pathLength = len(path[0])
    #     pickedPath1 = random.randint(0, numPaths - 1)
    #     pickedPath2 = random.randint(0, numPaths - 1)
    #     i1 = random.randint(1, pathLength - 1)
    #     i2 = random.randint(1, pathLength - 1)
    #     # swap
    #     temp = path[pickedPath1][i1]
    #     path[pickedPath1][i1] = path[pickedPath2][i2]
    #     path[pickedPath2][i2] = temp


    # """
    # setOfPaths: Helper method for createGeneration. Creates a random 
    #             individual for a new generation. One path per pacman.
    # @param 
    # @return paths: a 2d array of dimension n x m with 
    #                     n = # pacmen and m = # food
    # """
    # def setOfPaths(self, pacsList, foodList):
    #     paths = []
    #     random.shuffle(foodList)
    #     size = int(len(foodList)/len(pacsList))
    #     # add the pacman first
    #     for pac in pacsList:
    #         paths.append([pac])
    #         for i in range(size):
    #             paths[-1].append(foodList.pop())
    #     # add the food in random assignments to each path in the set
    #     while len(foodList) > 0:
    #         for path in paths:
    #             if len(foodList) > 0:
    #                 path.append(foodList.pop())
    #             else:
    #                 path.append((-1, -1))
    #     return paths

    # """
    # createGeneration: Creates a random generation.
    # @param  population: an integer of the number of individuals
    #         pacsList: a copy of the list of pacmen (as coords)
    #         foodList: a copy of the list of food (as coords)
    # @return generation: a 3d array of dimension g x n x m with 
    #                     g = population, n = # pacmen, and m = # food
    # """
    # def createGeneration(self, population, pacsList, foodList):
    #     return [self.setOfPaths(list(pacsList), list(foodList)) for _ in range(population)]


 
