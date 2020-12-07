import random
import numpy as np


class BaseAgent:
    max_energy_init = 100
    min_energy_init = 60
    fighting_capability_mean = 0.5
    fighting_energy_cost_base = 10
    fighting_energy_cost_factor = 5
    energy_from_cannibalising = 10
    energy_retained_when_cannibalising = 0.5
    mating_energy = 0.5
    mating_cost = 0.3

    def __init__(self, u):
        self.energy_max = 100
        self.alive = True
        self.energy = random.randint(self.min_energy_init, self.max_energy_init)
        self.u = u  # probability of committing cannibalism
        self.fighting_capability = np.random.randn() + self.fighting_capability_mean

    def fight(self, other):
        """Returns True if the individual wins"""
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

    # other should be returned as well!
    def interact(self, other):
        """returns
        - 0  if both survive
        - 1 if other dies
        - 2 if self dies
        - 3 if mate
        """
        r = random.random()
        if self.energy > self.mating_energy*self.energy_max and other.energy > other.mating_energy*other.energy_max:
            # Mate
            return 3, other
        elif r < self.u or r < other.u:
            outcome = self.fight(other)
            if outcome:
                self.cannibalise(other.energy)
                return 1, other
            else:
                other.cannibalise(self.energy)
                return 2, other
        return 0, other

    def eat(self, food_energy):
        self.change_energy(food_energy)

    def cannibalise(self, others_energy):
        # Assumes base case is not to cannibalise
        pass

    def mate(self, other):
        r = random.random()
        if r < 0.5:
            new_individual = type(self)(self.u)
        else:
            new_individual = type(other)(other.u)
        self.change_energy(-self.mating_cost*self.energy_max)
        other.change_energy(-other.mating_cost * other.energy_max)
        return new_individual

    def change_energy(self, amount):
        self.energy = min(self.energy + amount, self.energy_max)
