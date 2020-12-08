import numpy as np
import math
import time

def get_ind_population(population, Cannibalist):
    population_size = len(population)
    nr_can = 0
    nr_reg = 0

    for i in range(population_size):
        if type(population[i]) == Cannibalist:
            nr_can += 1
        else:
            nr_reg += 1

    return nr_can, nr_reg

def creep_mutation(u):
    return min(1, u + np.random.uniform(-0.05, 0.05))

def get_average_u(population):
    total = 0
    for i in range(len(population)):
        total += population[i].u
    average = total / len(population)
    return average

def get_average_p_cannibalize(population):
    total = 0
    for i in range(len(population)):
        total += population[i].p_cannibalise
    average = total / len(population)
    return average

def get_smallest_distance(individual, food_list):
    
    distances = list()
    for i in range(len(food_list)):
        
        x_diff = individual.x - food_list[i][0]
        y_diff = individual.y - food_list[i][1]
        distance = np.sqrt(x_diff**2 + y_diff**2)
        distances.append(distance)

    return distances.index(min(distances)), min(distances)

def get_distances(individual, population):
    distances = np.zeros(len(population))
    for i in range(len(population)):
        x_diff = individual.x - population[i].x
        y_diff = individual.y - population[i].y
        distance = np.sqrt(x_diff**2 + y_diff**2)
        ditances[i] = distance
    
    return distances


def get_adj_matrix(population):
    start= time.time()
    adj = np.zeros((len(population), len(population)))
    x = np.array([ind.x for ind in population]).reshape(-1, 1)
    x_diff = (x-x.transpose())**2
    y = np.array([ind.y for ind in population]).reshape(-1, 1)
    y_diff = (y - y.transpose()) ** 2
    adj = np.sqrt(x_diff+y_diff)
    np.fill_diagonal(adj, np.inf)
    end = time.time()
    print(end-start)
    return adj

def move(individual, gridsize):
    r = np.random.random()
    if r <= 1/4:
        individual.x = (individual.x + 1) % gridsize
    elif r <= 1/2:
        individual.x = (individual.x - 1) % gridsize
    elif r <= 3/4:
        individual.y = (individual.y + 1) % gridsize
    else:
        individual.y = (individual.y - 1) % gridsize

