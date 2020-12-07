import matplotlib.pyplot as plt 
import numpy as np
import math

def plot_nr(nr_can, nr_reg):
    plt.figure()
    plt.plot(nr_can, 'r', label="Cannibals")
    plt.plot(nr_reg, 'b', label="Regular")
    plt.legend()
    plt.xlabel("time step")
    plt.ylabel("population size")
    plt.title("Population size")
    plt.show()

def plot_rates(average_u, avarege_fight):
    plt.figure()
    plt.plot(average_u, 'r', label="Cannibalism rate")
    plt.plot(avarege_fight, 'b', label="Fight parameter")
    plt.legend()
    plt.xlabel("time step")
    plt.ylabel(" what to write here")
    plt.title("Change of evolutionary parameters")
    plt.show()
