from src.base_agent import BaseAgent
import random


class Cannibalist(BaseAgent):

    def eat(self, food_energy, other, other_dead=False):
        if not other_dead:
            self.change_energy(food_energy/2)
            other.change_energy(food_energy/2)
        else:
            r = random.random()
            if self.p_cannibalise is None or r < self.p_cannibalise:
                self.cannibalise(other.energy)
            else:
                self.change_energy(food_energy)

    def cannibalise(self, others_energy):
        # factor find in literature how much we can maintain of others energy
        self.change_energy(others_energy * self.energy_retained_when_cannibalising)
