from src.base_agent import BaseAgent


class Cannibalist(BaseAgent):

    def eat(self, food_energy, other=None):
        if other:
            self.change_energy(food_energy/2)
            other.change_energy(food_energy/2)
        else:
            # eat other instead
            pass

    def cannibalise(self, others_energy):
        # factor find in literature how much we can maintain of others energy
        self.change_energy(others_energy * self.energy_retained_when_cannibalising)
