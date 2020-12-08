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
import time

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
                if offspring:
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
    population = list()
    nr_time_steps = 300
    food_energy = 30
    metabolism = -5
    nr_cannibalists = list()
    average_u_list = list()
    average_p_list = list()
    grid_size = 100
    food_list = list()
    food_supply_list = list()
    init_food_supply = 30
    food_supply = init_food_supply

    # initialize population
    for i in range(ind_population):
        x = np.random.randint(grid_size)
        y = np.random.randint(grid_size)
        cannibal = Cannibalist(0.05, 0.6, 0.1, x, y)
        population.append(cannibal)
    
    # initialize food
    food_array = np.zeros((grid_size, grid_size))
    x = np.random.randint(grid_size, size=food_supply)
    y = np.random.randint(grid_size, size=food_supply)
    for _x, _y in zip(x, y):
        food_array[_x, _y] += 1
    food_list = list(zip(*food_array.nonzero()))

    graphs.plot_lattice(food_list, population, grid_size)
    # main code 
    for i in range(nr_time_steps):

        print("time step: ", i)
        new_population = list()
        

        # get averages
        average_u = get_average_u(population)
        average_p_cannibalize = get_average_p_cannibalize(population)
        average_u_list.append(average_u)
        average_p_list.append(average_p_cannibalize)
        nr_cannibalists.append(len(population))
        competition_list = np.zeros(len(population))
        competition_list = np.subtract(competition_list, 1)

        # Adj matrix:
        Adj_matrix = get_adj_matrix(population)

        # Interaction between individuals
        mated = np.zeros(len(population), dtype=bool)
        for j in range(len(population)):
            if mated[j]:
                continue
            partner_dist = np.amin(Adj_matrix[j, :])
            if population[j].energy >= population[j].mating_energy*population[j].energy_max and partner_dist < 5:
                closest = np.where(Adj_matrix[j, :] == partner_dist)[0][0]
                population[j].x = population[closest].x
                population[j].y = population[closest].y
                offspring = population[j].mate(population[closest])
                if offspring:
                    new_population.append(offspring)
                    mated[closest] = True
            else:
                
                index, distance = get_smallest_distance(population[j], food_list)
                r = random.random()
                if distance < 5:
            
                    population[j].x = food_list[index][0]
                    population[j].y = food_list[index][1]
                    competition_list[j] = index

                elif r < population[j].p_cannibalise*(population[j].energy_max/(population[j].energy * 10)) and partner_dist < 5:
                    closest = np.where(Adj_matrix[j, :] == partner_dist)[0][0]
                    population[j].x = population[closest].x
                    population[j].y = population[closest].y
                    outcome = population[j].fight(population[closest])
                    if outcome:
                        population[j].cannibalise(population[closest].energy)
                    else:
                        population[closest].eat(0, population[j], other_dead=True)
                else: 
                    move(population[j], grid_size)

            new_population.append(population[j])

        # interact
        food_index_to_remove = []
        start = time.time()
        for k in range(len(food_list)):
            indices = [v for v, x in enumerate(competition_list) if x == k and population[v].alive and not mated[v]]
            coord_x, coord_y = food_list[k][0], food_list[k][1]
            food_at_coord = food_array[coord_x, coord_y]
            if len(indices) != 0:
                """if len(indices) == 1:
                    population[indices[0]].consume_food(food_energy)
                    food_index_to_remove.append(k)
                    food_array[food_list[k][0], food_list[k][1]] -= 1
                el"""
                if food_at_coord >= len(indices):
                    for agent_index in indices:
                        population[agent_index].consume_food(food_energy)
                        food_array[coord_x, coord_y] -= 1
                else:
                    selected_food = np.random.randint(food_at_coord, size=len(indices))
                    for i in range(int(food_at_coord)):
                        agents_index = np.where(selected_food == i)[0]
                        agents_to_compete = [population[indices[index]] for index in agents_index]
                        if len(agents_to_compete) == 1:
                            agents_to_compete[0].consume_food(food_energy)
                            food_left = 0
                            food_array[coord_x, coord_y] -= 1
                        elif len(agents_to_compete) == 2:
                            _, food_left = agents_to_compete[0].interact(agents_to_compete[1], food_energy)
                        elif len(agents_to_compete) > 2:
                            _, food_left = agents_to_compete[0].interact(agents_to_compete[1:], food_energy)
                        if food_left:
                            food_array[coord_x, coord_y] -= 1
        end = time.time()
        print(end - start)

        #food_list = [coord for _index, coord in enumerate(food_list) if _index not in food_index_to_remove]
          
        # spawn new food
        x = np.random.randint(grid_size, size=food_supply)
        y = np.random.randint(grid_size, size=food_supply)
        for _x, _y in zip(x,y):
            food_array[_x, _y] += 1
        food_list = list(zip(*food_array.nonzero()))

        # Lose energy every timestep
        for j in range(len(new_population)):
            new_population[j].change_energy(metabolism)

        # save population
        population = [agent for agent in new_population if agent.energy > 0 and agent.alive]
        dead_by_energy = np.array([1 for agent in new_population if agent.energy <= 0]).sum()
        print(f"dead_by_energy {dead_by_energy}")
        dead_by_fight = np.array([1 for agent in new_population if not agent.alive]).sum()
        print(f"dead_by_fight {dead_by_fight}")
        print(len(population))
        mod_food_supply =graphs.plot_lattice(food_list, population, grid_size)
        food_supply = int(round(init_food_supply*mod_food_supply))
        food_supply_list.append(food_supply)
    graphs.plot_rates(average_u_list, average_p_list, food_supply_list)



if __name__ == '__main__':
    #cannibal_regular()
    evolution_simulation()
