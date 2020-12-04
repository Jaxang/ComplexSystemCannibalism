from src.cannibalist import Cannibalist



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

