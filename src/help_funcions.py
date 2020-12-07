from src.cannibalist import Cannibalist
import numpy as np
import math

def get_ind_population(population):
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
    return u + np.random.uniform(-0.01, 0.01)

def get_average_u(population):
    total = 0
    for i in range(len(population)):
        total += population[i].u
    average = total / len(population)
    return average

def get_average_p_cannibalize(population):
    total = 0
    for i in range(len(population)):
        total += population[i].p_cannabilize
    average = total / len(population)
    return average