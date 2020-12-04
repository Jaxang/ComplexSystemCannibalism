from src.cannibalist import Cannbialist


individual1 = Cannibalist(1)
individual2 = Cannibalist(1)


individual1.figthing_capability = 0
individual2.figthing_capability = 1


print(individual1.fight(individual2))

