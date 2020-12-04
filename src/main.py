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
    metabolism = -4

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
        new_population = list()
        random.shuffle(population)

        #TODO: plot size of 

        # Interaction between individuals
        if len(population) % 2 == 0: # if population is even
            for j  in range(0,len(population), 2):

                return_code, other = population[j].interact(population[j+1]) # 0 both survive, 1 - other dies, 2 self dies 3 - reproduce
                if return_code == 0:
                    new_population.append(population[j])
                    new_population.append(population[j+1])
                if return_code == 1:
                    new_population.append(population[j])
                if return_code == 2:
                    new_population.append(other)
                if return_code == 3:
                    offspring = population[j].mate(population[j+1]) # will changes be made to population[j+1] ? 
                    new_population.append(population[j])
                    new_population.append(population[j+1])
                    new_population.append(offspring)

        else:   # is uneven
            for j in range(0,len(population) - 1, 2):

                return_code, other = population[j].interact(population[j+1]) # 0 both survive, 1 - other dies, 2 self dies 3 - reproduce
                
                if return_code == 0:
                    new_population.append(population[j])
                    new_population.append(population[j+1])
                if return_code == 1:
                    new_population.append(population[j])
                if return_code == 2:
                    new_population.append(other)
                if return_code == 3:
                    offspring = population[j].mate(population[j+1])
                    new_population.append(population[j])
                    new_population.append(population[j+1])
                    new_population.append(offspring)

        # Lose energy every timestep
        for i in range(len(new_population)):
            new_population[i].change_enery(metabolism)
        

        population = np.copy(new_population)

