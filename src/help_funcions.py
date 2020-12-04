from cannabalist import Cannabalist



def get_ind_population(population):
    population_size = length(population)
    nr_can = population.count(Cannabalist) 
    nr_non = population_size - nr_can # None-cannabalist
    
    return nr_can, nr_non
        
