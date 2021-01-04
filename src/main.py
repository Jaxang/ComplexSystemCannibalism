from src.help_funcions import get_ind_population, get_adj_matrix
from src.help_funcions import get_average_u
from src.help_funcions import get_average_u
from src.help_funcions import get_average_p_cannibalize
from src.help_funcions import get_smallest_distance
from src.help_funcions import move
from src.help_funcions import get_nearby_food
from src.cannibalist import Cannibalist
from src.regular import Regular
import src.graphs as graphs
import random
import matplotlib.pyplot as plt
import numpy as np
import time
from multiprocessing import Process, Queue
from numpy import asarray
from numpy import savetxt

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

def lattice_model(plot = True, init_food_supply = 30, p_cannibalise = 0.1, nr_time_steps=1000):
    ind_population = 100
    population = list()
    food_energy = 10
    metabolism = -0.1
    nr_cannibalists = list()
    average_u_list = list()
    average_p_list = list()
    available_food = list()
    population_size = list()
    grid_size = 100
    food_list = list()
    food_supply_list = list()
    
    food_supply = init_food_supply
    search_area = 5

    # initialize population
    for i in range(ind_population):
        x = np.random.randint(grid_size)
        y = np.random.randint(grid_size)
        cannibal = Cannibalist(0.05, 0.6, p_cannibalise, x, y)
        population.append(cannibal)
    
    # initialize food
    food_array = np.zeros((grid_size, grid_size))
    x = np.random.randint(grid_size, size=int(food_supply))
    y = np.random.randint(grid_size, size=int(food_supply))
    for _x, _y in zip(x, y):
        food_array[_x, _y] += 1
    food_list = list(zip(*food_array.nonzero()))
    if plot:
        graphs.plot_lattice(food_list, population, grid_size)
    # main code 
    for i in range(nr_time_steps):
        if len(population) == 0:
            break
        #print("time step: ", i)
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
                
                #index, distance = get_smallest_distance(population[j], food_list)
                indices = get_nearby_food(population[j], food_list, search_area)

                r = random.random()
                if len(indices) > 0:

                    rand = np.random.randint(0,len(indices))
                    index = indices[rand]
                    population[j].x = food_list[index][0]
                    population[j].y = food_list[index][1]
                    competition_list[j] = index

                elif population[j].energy > 0 and population[j].energy < 20 and r < population[j].p_cannibalise and partner_dist < 5:
                    closest = np.where(Adj_matrix[j, :] == partner_dist)[0][0]
                    population[j].x = population[closest].x
                    population[j].y = population[closest].y
                    outcome = population[j].fight(population[closest])
                    if outcome:
                        population[j].cannibalise(population[closest].energy)
                    else:
                        population[closest].eat(0, population[j], other_dead=True)
                else: 
                    for _ in range(5):
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
                        food_left = 1
                        if len(agents_to_compete) == 1:
                            agents_to_compete[0].consume_food(food_energy)
                            food_left = 0
                        elif len(agents_to_compete) == 2:
                            _, food_left = agents_to_compete[0].interact(agents_to_compete[1], food_energy)
                        elif len(agents_to_compete) > 2:
                            _, food_left = agents_to_compete[0].interact(agents_to_compete[1:], food_energy)
                        if food_left == 0:
                            food_array[coord_x, coord_y] -= 1
        end = time.time()
        #print(end - start)

        #food_list = [coord for _index, coord in enumerate(food_list) if _index not in food_index_to_remove]

        available_food.append(food_array.sum())
        population_size.append(len(population))

        # spawn new food
        """if i == nr_time_steps//2:
            food_supply = food_supply//2
        elif i == (3*nr_time_steps)//4:
            food_supply = init_food_supply//4"""

        x = np.random.randint(grid_size, size=int(food_supply))
        y = np.random.randint(grid_size, size=int(food_supply))
        for _x, _y in zip(x,y):
            food_array[_x, _y] += 1
        food_list = list(zip(*food_array.nonzero()))

        # Lose energy every timestep
        for j in range(len(new_population)):
            new_population[j].change_energy(metabolism)

        # save population
        population = [agent for agent in new_population if agent.energy > 0 and agent.alive]
        dead_by_energy = np.array([1 for agent in new_population if agent.energy <= 0]).sum()
        # print(f"dead_by_energy {dead_by_energy}")
        dead_by_fight = np.array([1 for agent in new_population if not agent.alive]).sum()
        # print(f"dead_by_fight {dead_by_fight}")
        # print(len(population))
        if plot:
            mod_food_supply =graphs.plot_lattice(food_list, population, grid_size)
            food_supply = int(round(init_food_supply*mod_food_supply))
        food_supply_list.append(food_supply)

    if plot:
        graphs.plot_rates(average_u_list, average_p_list, food_supply_list)
    else:
        return len(population), available_food, population_size


def simulation_run(q, food_supply):
    
    nr_averages = 5
    nr_threads = 8
    p_cannibalise = np.linspace(0.05, 0.5, nr_threads)
    temp_survivors = np.zeros(nr_averages)
    nr_survivors = np.zeros(len(p_cannibalise))

    for i in range(len(p_cannibalise)):
        for j in range(nr_averages):
            temp_survivors[j] = lattice_model(False, food_supply, p_cannibalise[i])[0]
        nr_survivors[i] = np.sum(temp_survivors) / nr_averages
    q.put(nr_survivors)

def parameter_search():
    nr_threads = 8
    p_cannibalise = np.linspace(0, 0.5, nr_threads)
    food_source = np.linspace(5,50,nr_threads*2)
    queues = list()
    processes = list()
    save_survivors = np.zeros((len(p_cannibalise), len(food_source)))
    proc = 0

    for i in range(2):
        for j in range(nr_threads):
            queues.append(Queue())
            processes.append(Process(target = simulation_run,args=(queues[i*nr_threads+j],
            food_source[i*nr_threads+j],)))
        print("start")
        # start processes
        for j in range(nr_threads):
            processes[i*nr_threads+j].start()
        print("join")
        # join processes
        for j in range(nr_threads):
            processes[i * nr_threads + j].join()

        print("save")
        # save values
        for j in range(nr_threads):
            print("i:" ,i )
            print("j:", j)
            save_survivors[:, i* nr_threads+j] = np.transpose(queues[i*nr_threads + j].get())
            print("lal")
        proc += 1
        print(proc)
    data = asarray(save_survivors)
    savetxt('survivors.csv', data, delimiter=',')


def simulation_run2(q, food_supply, time_steps, p_cannibalise):
    nr_averages = 10
    temp_food = np.zeros((time_steps, nr_averages))
    temp_population = np.zeros((time_steps, nr_averages))

    for j in range(nr_averages):
        print(f"pcan={p_cannibalise}, j={j}")
        output = lattice_model(False, food_supply, p_cannibalise, time_steps)
        temp_food[:, j] = np.array(output[1])
        temp_population[:, j] = np.array(output[2])
        print("average done: " , j)
    food_per_time_step = temp_food.mean(1)
    pop_per_time_step = temp_population.mean(1)
<<<<<<< HEAD
    print("queue put")
=======
    print(f"pcan={p_cannibalise}, putting")
>>>>>>> c4bd8208baeb5c76134afc39c8cd2200c6b5c67f
    q.put((food_per_time_step, pop_per_time_step))
    print(f"pcan={p_cannibalise}, done")


def parameter_search2():
    nr_threads = 12
    p_cannibalise = np.linspace(0, 0.2, nr_threads)
    food_source = 12
    time_steps = 5000
    queues = list()
    processes = list()
    save_food = np.zeros((len(p_cannibalise), time_steps))
    save_pop = np.zeros((len(p_cannibalise), time_steps))
    proc = 0

    for j in range(nr_threads):
        queues.append(Queue())
        processes.append(Process(target=simulation_run2, args=(queues[j], food_source, time_steps, p_cannibalise[j],)))
    print("start")
    # start processes
    for j in range(nr_threads):
        processes[j].start()

    print("save")
    # save values
    for j in range(nr_threads):
        print("j:", j)
        output = queues[j].get()
        save_food[j, :] = np.transpose(output[0])
        save_pop[j, :] = np.transpose(output[1])
        print("lal")

    print("join")
    # join processes
    for j in range(nr_threads):
        print(f"join {j}")
        processes[j].join()
    proc += 1
    print(proc)
    data = asarray(save_food)
    savetxt(f'food_available_{time_steps}_short_0-2.csv', data, delimiter=',')
    data = asarray(save_pop)
    savetxt(f'population_{time_steps}_short_0-2.csv', data, delimiter=',')

def plot_func():
    graphs.plot_surface()

if __name__ == '__main__':
    #cannibal_regular()
    evolution_simulation()
