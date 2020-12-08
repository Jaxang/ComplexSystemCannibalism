import random
import numpy as np

from src.help_funcions import creep_mutation


class BaseAgent:
    max_energy_init = 100
    min_energy_init = 60
    fighting_capability_mean = 0.5
    fighting_energy_cost_base = 10
    fighting_energy_cost_factor = 5
    energy_from_cannibalising = 10
    energy_retained_when_cannibalising = 0.85
    mating_energy = 0.5
    mating_cost = 0.3
    

    def __init__(self, u, f, p_cannibalise=None, x = 1, y = 1):
        self.energy_max = 100
        self.alive = True
        self.energy = 49
        self.u = u  # probability of committing cannibalism
        self.fighting_capability = f
        self.p_cannibalise = p_cannibalise
        self.x = x
        self.y = y

    def fight(self, other):
        """Returns True if the individual wins"""
        if not type(other) == list:
            total_cap = self.fighting_capability + other.fighting_capability
            cap_diff = self.fighting_capability - other.fighting_capability

            capability_cost = cap_diff * self.fighting_energy_cost_factor
            r = random.random()
            if r < self.fighting_capability/total_cap:
                # self wins
                energy_cost = self.fighting_energy_cost_base - capability_cost
                self.change_energy(-energy_cost)
                other.alive = False
                return True
            else:
                # other wins
                energy_cost = self.fighting_energy_cost_base + capability_cost
                other.change_energy(-energy_cost)
                self.alive = False
                return False
        else:
            all_agents = other + [self]
            capabilites = np.array([agent.fighting_capability for agent in all_agents])
            capabilites_norm = capabilites.cumsum()/capabilites.sum()
            r = random.random()
            index = None
            for i, cap in enumerate(capabilites_norm):
                if r < cap and not index:
                    _agent = all_agents[i]
                    index = i
                    cost = (2*_agent.fighting_capability - capabilites.sum())*_agent.fighting_energy_cost_factor
                    _agent.change_energy(_agent.fighting_energy_cost_base - cost)
                else:
                    q = random.random()
                    if q < 0.7:
                        all_agents[i].alive = False
            return index


    # other should be returned as well!
    def interact(self, other, food):
        """returns
        - 0  if both survive
        - 1 if other dies
        - 2 if self dies
        - 3 if mate
        """
        if not type(other) == list:
            r = random.random()
            if self.energy > self.mating_energy*self.energy_max and other.energy > other.mating_energy*other.energy_max:
                # Mate
                return 3, other
            elif r < self.u or r < other.u:
                outcome = self.fight(other)
                if outcome:
                    food_left = self.eat(food, other, other_dead=True)
                    return 1, food_left
                else:
                    food_left = other.eat(food, self, other_dead=True)
                    return 2, food_left
            else:
                food_left = self.eat(food, other, other_dead=False)
            return 0, food_left
        else:
            r = random.random()
            all_agents = other + [self]
            if any([r < agent.u for agent in all_agents]):
                outcome = self.fight(other)
                dead_agents = [agent.energy if not agent.alive else -1 for i, agent in enumerate(all_agents)]
                agent_to_eat = dead_agents.index(max(dead_agents))
                food_left = all_agents[outcome].eat(food, all_agents[agent_to_eat], other_dead=True)
                return outcome, food_left
            else:
                for _agent in all_agents:
                    _agent.change_energy(food/len(all_agents))
                return 0, 0


    def eat(self, food_energy, other, other_dead=False):
        pass

    def cannibalise(self, others_energy):
        # Assumes base case is not to cannibalise
        pass

    def consume_food(self, food_energy):
        self.change_energy(food_energy)

    def mate(self, other):
        r = random.random()
        if self.energy > self.mating_energy*self.energy_max and other.energy > other.mating_energy*other.energy_max:
            if r < 0.5:
                new_p_cannibalise = creep_mutation(self.p_cannibalise) if self.p_cannibalise else None
                new_individual = type(self)(self.u, self.fighting_capability, new_p_cannibalise, x=self.x, y=self.y)
            else:
                new_p_cannibalise = creep_mutation(other.p_cannibalise) if other.p_cannibalise else None
                new_individual = type(other)(other.u, other.fighting_capability, new_p_cannibalise, x=other.x, y=other.y)

            self.change_energy(-self.mating_cost*self.energy_max)
            other.change_energy(-other.mating_cost * other.energy_max)
            return new_individual

    def change_energy(self, amount):
        self.energy = min(self.energy + amount, self.energy_max)
