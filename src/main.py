from src.help_funcions import get_ind_population, get_adj_matrix
from src.help_funcions import get_average_u
from src.help_funcions import get_average_u
from src.help_funcions import get_average_p_cannibalize
from src.help_funcions import get_smallest_distance
from src.help_funcions import move
from src.cannibalist import Cannibalist
from src.regular import Regular
import src.graphs as graphs
import random
import matplotlib.pyplot as plt
import numpy as np

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
        print("time step: ", i)
        new_population = list()
        random.shuffle(population)
        
        # save nr_cannibals, save nr_regulars
        nr_can, nr_reg = get_ind_population(population, Cannibalist)
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

"""
------------------------------------------------------------------------------------------------------------------------------------
                    Evolution simulation
"""
def evolution_simulation():
    ind_population = 100
    cannibalists = list()
    regulars = list()
    population = list()
    nr_time_steps = 3000
    food_sorce = 2 * 20 * ind_population
    metabolism = -5
    nr_cannibalists = list()
    average_u_list = list()
    average_p_list = list()

    # initialize population
    for i in range(ind_population):
        cannibal = Cannibalist(0.3, 0.6, 0.1)
        population.append(cannibal)

    # main code 
    for i in range(nr_time_steps):
        print("time step: ", i)
        new_population = list()
        random.shuffle(population)
        
        # get averages
        average_u = get_average_u(population)
        average_p_cannibalize = get_average_p_cannibalize(population)
        average_u_list.append(average_u)
        average_p_list.append(average_p_cannibalize)
        nr_cannibalists.append(len(population))
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
                offspring = population[j].mate(population[j+1]) 
                new_population.append(population[j])
                new_population.append(other)
                new_population.append(offspring)

        # Lose energy every timestep
        for j in range(len(new_population)):
            new_population[j].change_energy(metabolism)
        
        population = [j for j in new_population if j.energy > 0]

    graphs.plot_rates(average_u_list, average_p_list, nr_cannibalists)

def lattice_model():
    ind_population = 100
    cannibalists = list()
    population = list()
    nr_time_steps = 3000
    food_source = 2 * 20 * ind_population
    food_energy = 10
    metabolism = -5
    nr_cannibalists = list()
    average_u_list = list()
    average_p_list = list()
    grid_size = 100
    food_list = list()
    food_supply = 30

    # initialize population
    for i in range(ind_population):
        x = np.random.randint(grid_size)
        y = np.random.randint(grid_size)
        cannibal = Cannibalist(0.3, 0.6, 0.1,x, y)
        population.append(cannibal)
    
    # initialize food
    for i in range(food_supply):
        x = np.random.randint(grid_size)
        y = np.random.randint(grid_size)
        food_list.append([x,y])


    # main code 
    for i in range(nr_time_steps):

        print("time step: ", i)
        new_population = list()
        
        graphs.plot_lattice(food_list, population, grid_size)
        # get averages
        average_u = get_average_u(population)
        average_p_cannibalize = get_average_p_cannibalize(population)
        average_u_list.append(average_u)
        average_p_list.append(average_p_cannibalize)
        nr_cannibalists.append(len(population))
        nr_interactions = len(population) - len(population) // 2
        food_per_interaction = food_source/nr_interactions
        competition_list = np.zeros(len(population))
        competition_list = np.subtract(competition_list,1)

        # Adj matrix:
        Adj_matrix = get_adj_matrix(population)

        # Interaction between individuals
        for j in range(len(population)):
            
            if population[j].energy >= population[j].mating_energy*population[j].energy_max:
                
                partner_dist = np.amin(Adj_matrix[j, :])

                if partner_dist < 5:
                    closest = np.where(Adj_matrix[j, :] == partner_dist)[0][0]
                    population[j].x = population[closest].x
                    population[j].y = population[closest].y
                    offspring = population[j].mate(population[closest])
                    new_population.append(offspring)
            else:
                
                index, distance = get_smallest_distance(population[j], food_list)

                if distance < 5:
            
                    population[j].x = food_list[index][0]
                    population[j].y = food_list[index][1]
                    competition_list[j] = index

                else: 
                    move(population[j], grid_size)

            new_population.append(population[j])

        # interact
        index_to_remove=[]
        for k in range(len(food_list)):
            indices = [v for v, x in enumerate(competition_list) if x == k]
            if len(indices) != 0:
                if len(indices) == 1:
                    population[indices[0]].consume_food(food_energy)
                    index_to_remove.append(k)
                else:
                    indices = np.random.choice(indices, 2)
                    _, food_left = population[indices[0]].interact(population[indices[1]], food_energy)
                    if food_left == 0:
                        index_to_remove.append(k)
        food_list = [coord for _index, coord in enumerate(food_list) if _index in index_to_remove]
          
        # spawn new food
        for j in range(food_supply):
            x = np.random.randint(grid_size)
            y = np.random.randint(grid_size)
            food_list.append([x,y])

        # Lose energy every timestep
        for j in range(len(new_population)):
            new_population[j].change_energy(metabolism)

        # save population
        population = [j for j in new_population if j.energy > 0]



if __name__ == '__main__':
    #cannibal_regular()
    evolution_simulation()
