from .base_agent import BaseAgent
from .regular import Regular
import random


class Cannibalist(BaseAgent):

    def cannibalise(self, others_energy):
        # factor find in literature how much we can maintain of others energy
        self.change_energy(others_energy * self.energy_retained_when_cannibalising)
