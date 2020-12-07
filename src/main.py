from src.help_funcions import get_ind_population
from src.cannibalist import Cannibalist
from src.regular import Regular
import src.graphs as graphs
import random


def cannibal_regular():
    ind_population = 100
    cannibalists = list()
    regulars = list()
    population = list()
    nr_time_steps = 300
    food_sorce = 2 * 20 * ind_population
    metabolism = -5
    nr_cannibalists = list()
    nr_regulars = list()

    # initialize population
    for i in range(ind_population):
        cannibal = Cannibalist(0.3, 0.6)
        regular = Regular(0, 0.3)
        cannibalists.append(cannibal)
        regulars.append(regular)

    population.extend(cannibalists)
    population.extend(regulars)

    # main code 
    for i in range(nr_time_steps):
        print(i)
        new_population = list()
        random.shuffle(population)

        # save nr_cannibals, save nr_regulars
        nr_can, nr_reg = get_ind_population(population)
        nr_cannibalists.append(nr_can)
        nr_regulars.append(nr_reg)
        nr_interactions = len(population) - len(population) // 2
        food_per_interaction = food_sorce/nr_interactions

        # Interaction between individuals
        for j in range(0, len(population) - len(population) % 2, 2):

            return_code, other = population[j].interact(population[j+1], food_per_interaction) # 0 both survive, 1 - other dies, 2 self dies 3 - reproduce
            if return_code == 0:
                new_population.append(population[j])
                new_population.append(other)
            elif return_code == 1:
                new_population.append(population[j])
            elif return_code == 2:
                new_population.append(other)
            elif return_code == 3:
                offspring = population[j].mate(population[j+1]) # will changes be made to population[j+1] ? 
                new_population.append(population[j])
                new_population.append(other)
                new_population.append(offspring)

        # Lose energy every timestep
        for j in range(len(new_population)):
            new_population[j].change_energy(metabolism)
        
        population = [j for j in new_population if j.energy > 0]

    graphs.plot_nr(nr_cannibalists, nr_regulars)


if __name__ == '__main__':
    cannibal_regular()
