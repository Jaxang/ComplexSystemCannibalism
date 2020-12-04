import help_funcions
from cannibalist import Cannibalist
from regular import Regular
import graphs
import random



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
        random.shuffle(population)
        if len(population) % 2 == 0: # if population is even
            for j  in range(0,len(population), 2):
                tournament(population[j], population[j+1]

        else:   # is uneven
            for j in range(0,len(population) - 1, 2):
                
        
            

    