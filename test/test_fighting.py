from src.cannibalist import Cannibalist


individual1 = Cannibalist(1)
individual2 = Cannibalist(1)


individual1.fighting_capability = 0
individual2.fighting_capability = 1
individual1.energy = 49
individual2.energy = 49

print(individual1.fight(individual2))
assert individual2.energy == 44
individual2.cannibalise(individual1.energy)
assert individual2.energy == 68.5
