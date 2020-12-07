import matplotlib.pyplot as plt 


def plot_nr(nr_can, nr_reg):
    print(f"Number of cannibals: {nr_can} \nNumber of regulars: {nr_reg}")
    plt.figure()
    plt.plot(nr_can, 'r', label="Cannibals")
    plt.plot(nr_reg, 'b', label="Regular")
    plt.legend()
    plt.xlabel("time step")
    plt.ylabel("population size")
    plt.title("Population size")
    plt.show()
