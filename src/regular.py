from src.base_agent import BaseAgent


class Regular(BaseAgent):

    def eat(self, food_energy, other, other_dead=False):
        if not other_dead:
            self.change_energy(food_energy/2)
            other.change_energy(food_energy/2)
        else:
            self.change_energy(food_energy)
