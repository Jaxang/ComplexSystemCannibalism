import numpy as np
import math

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
    adj = np.zeros((len(population) +1, len(population)+1))
    for i in range(len(population)):
        for j in range(i, len(population)):
            if i == j:
                adj[i,j] = math.inf
                adj[j,i] = math.inf
            else:
                x_diff = population[i].x - population[j].x
                y_diff = population[i].y - population[j].y
                dist = np.sqrt(x_diff** + y_diff**2)
                adj[i,j] = dist
                adj[j,i] = dist
    
    return adj

def move(individual, gridsize):
    r = np.random.random
    if r <= 1/4:
        individual.x += 1
        if individual.x > gridsize:
            individual.x = 0
    elif r <= 1/2:
        individual.x -= 1
        if individual.x < 0:
            individual.x = gridsize
    elif r <= 3/4:
        individual.y += 1
        if individual.y > gridSize:
            individual.y = 0
    else:
        individual.y -= 1
        if individual.y < 0:
            individual.y = gridsize

