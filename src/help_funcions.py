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