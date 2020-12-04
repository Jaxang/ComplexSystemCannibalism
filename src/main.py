import help_funcions
from cannibalist import Cannibalist
from regular import Regular
import graphs
import random
import numpy as np
         


if __name__ == '__main__':

    ind_population = 100
    cannibalists = list()
    regulars = list()
    population = list()
    nr_time_steps = 1000

    # initialize population
    for i in range(ind_population):
        cannibal = Cannibalist(0.1)
        regular = Regular(0.1)
        cannibalists.append(cannibal)
        regulars.append(regular)

    population.extend(cannibalists)
    population.extend(regulars)

    # main code 
    for i in range(nr_time_steps):
        temp_population = np
        random.shuffle(population)
        if len(population) % 2 == 0: # if population is even
            for j  in range(0,len(population), 2):
                return_code = population[j].tournament(population[j+1]) # 0 both survive, 1 - other dies, 2 self dies 3 - reproduce
                if return_code == 1:
                    population.remove(j+1)
                if return_code == 2:
                    population.remove(j)
                if return_code == 3:
                    if type(population[j]) == Cannibalist:
                        cannibal = Cannibalist(0.1)
                        population.append(cannibal)
                    if type(population[j]) == Regular:
                        regular = Regular(0.1)
                        population.append(regular)


        else:   # is uneven
            for j in range(0,len(population) - 1, 2):
                
        
            

