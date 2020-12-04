from src.cannibalist import Cannibalist


def get_ind_population(population):
    population_size = len(population)
    nr_can = population.count(Cannibalist)
    nr_non = population_size - nr_can  # None-cannabalist
    
    return nr_can, nr_non

