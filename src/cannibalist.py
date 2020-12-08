from src.base_agent import BaseAgent
import random


class Cannibalist(BaseAgent):
    #return 0 if no food is left, 1 if the food is untouched.
    def eat(self, food_energy, other, other_dead=False):
        if not other_dead:
            self.change_energy(food_energy/2)
            other.change_energy(food_energy/2)
            return 0
        else:
            r = random.random()
            if self.p_cannibalise is None or r < self.p_cannibalise:
                self.cannibalise(other.energy)
                return 1
            else:
                self.change_energy(food_energy)
                return 0

    def cannibalise(self, others_energy):
        # factor find in literature how much we can maintain of others energy
        self.change_energy(others_energy * self.energy_retained_when_cannibalising)
