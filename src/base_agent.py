import random
import numpy as np


class BaseAgent:
    max_energy_init = 100
    min_energy_init = 60
    fighting_capability_mean = 0.5
    fighting_energy_cost_base = 10
    fighting_energy_cost_factor = 5

    def __init__(self, u):
        self.energy_max = 100
        self.energy = random.randint(self.min_energy_init, self.max_energy_init)
        self.u = u  # probability of comitting cannibalism
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
            return True
        else:
            # other wins
            energy_cost = self.fighting_energy_cost_base + capability_cost
            return False

    def interact(self, other):
        raise NotImplementedError
