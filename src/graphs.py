import matplotlib.pyplot as plt 
import numpy as np
import math

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

def plot_rates(average_u, averege_fight, population_size):
    plt.figure()
    plt.subplot(121)
    plt.plot(average_u, 'r', label="Cannibalism rate")
    plt.plot(averege_fight, 'b', label="Fight parameter")
    plt.subplot(122)
    plt.plot(population_size, 'g', population_size)
    plt.legend()
    plt.xlabel("time step")
    plt.ylabel(" what to write here")
    plt.title("Change of evolutionary parameters")
    plt.show()
   