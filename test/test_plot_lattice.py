import time

from src.graphs import plot_lattice


class agent_mock:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def test_plot_lattice():
    for i in range(10):
        pop_list = [agent_mock(10, 10), agent_mock(20, 20), agent_mock(20, 20), agent_mock(30, 30), agent_mock(30, 30), agent_mock(30, 30)]
        food_list = [(40, 40)]
        print(plot_lattice(food_list, pop_list))
        time.sleep(1)
    for i in range(10):
        pop_list = [agent_mock(10, 10), agent_mock(20, 20), agent_mock(20, 20), agent_mock(30, 30), agent_mock(30, 30), agent_mock(30, 30)]
        food_list = [(10, 10), (20, 20), (30, 30),  (40,40)]
        print(plot_lattice(food_list, pop_list))
        time.sleep(1)
    for i in range(10):
        pop_list = [agent_mock(10, 10), agent_mock(20, 20), agent_mock(20, 20), agent_mock(30, 30), agent_mock(30, 30), agent_mock(30, 30)]
        food_list = [(11, 11), (21, 21), (31, 31), (40, 40)]
        print(plot_lattice(food_list, pop_list))
        time.sleep(1)
test_plot_lattice()
