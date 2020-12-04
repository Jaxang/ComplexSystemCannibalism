from src.help_funcions import get_ind_population
from src.cannibalist import Cannibalist
from src.regular import Regular
import src.graphs as graphs
import random
import numpy as np
import copy


def main():
    ind_population = 100
    cannibalists = list()
    regulars = list()
    population = list()
    nr_time_steps = 1000
    metabolism = -4
    nr_cannibalists = list()
    nr_regulars = list()

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

        #save nr_cannibalists, save nr_regulars
        nr_can, nr_reg = get_ind_population(population)
        nr_cannibalists.append(nr_can)
        nr_regulars.append(nr_reg)

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
            new_population[i].change_energy(metabolism)

        
        population =  [i for i in new_population if i.energy > 0]
        


    graphs.plot_nr(nr_cannibalists, nr_regulars)


if __name__ == '__main__':
    main()