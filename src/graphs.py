import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from PIL import Image
from PIL import ImageTk as itk
from matplotlib import cm
from numpy import genfromtxt

class CanvasAnimate:
    def __init__(self, res=500, l=5):
        self.l = l
        self.res = res
        self.tk = Tk()
        self.tk.geometry(str(int(res * 1.1)) + 'x' + str(int(res * 1.3)))
        self.tk.configure(background='white')

        self.canvas = Canvas(self.tk, bd=2)  # Generate animation window
        self.tk.attributes('-topmost', 0)
        self.canvas.place(x=res / 20, y=res / 20, height=res, width=res)
        ccolor = ['#0008FF', '#DB0000', '#12F200']

        self.food = Scale(self.tk, from_=0, to=2, orient=HORIZONTAL, label='percentage food source', font=("Helvetica", 8),
                            resolution=0.01)
        self.food.place(relx=.57, rely=.85, relheight=0.12, relwidth=0.33)
        self.food.set(1)  # Parameter slider for lightning rate
        self.image = np.zeros((l, l, 3))

    def update(self, agent_array, food_array):
        # Nothing = black, food = green,
        # 1 agent = red,        1 agent + food = yellow,
        # 2 agent = magenta,    2 agent + food = white,
        # 3 agent = blue,       3 agent + food = cyan
        self.image[:,:,:] = 0
        self.image[:, :, 0] = (agent_array == 1)*255*1 + (agent_array == 2)*255 + (agent_array >= 3)*255*0
        self.image[:, :, 2] = (agent_array == 1)*255*0 + (agent_array == 2)*255 + (agent_array >= 3)*255
        self.image[:, :, 1] = (food_array > 0)*255
        img = itk.PhotoImage(Image.fromarray(np.uint8(self.image), 'RGB').resize((self.res, self.res)))
        self.canvas.create_image(0, 0, anchor=NW, image=img)
        self.tk.title('Lattice')
        self.tk.update()
        return self.food.get()


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
    plt.subplot(211)
    plt.plot(average_u, 'r', label="Cannibalism rate")
    plt.plot(averege_fight, 'b', label="Fight parameter")
    plt.subplot(212)
    plt.plot(population_size, 'g', population_size)
    plt.legend()
    plt.xlabel("time step")
    plt.ylabel(" what to write here")
    plt.title("Change of evolutionary parameters")
    plt.show()


canvas = None


def plot_lattice(food_list, population_list, l=100):
    global canvas
    if canvas is None:
        canvas = CanvasAnimate(l=l)
    agent_array = np.zeros((l,l))
    for agent in population_list:
        agent_array[agent.x, agent.y] += 1

    food_array = np.zeros((l,l))
    for x, y in food_list:
        food_array[x, y] += 1

    return canvas.update(agent_array, food_array)

def plot_surface():
    nr_threads = 12
    survivors = genfromtxt("src/survivors2.csv", delimiter=",")
    p_cannibalise = np.linspace(0.05, 0.5, nr_threads)
    food_source = np.linspace(5,20,nr_threads*2)



    fig = plt.figure()
    ax = fig.gca(projection="3d")
 
    X = food_source
    Y = p_cannibalise
    X, Y = np.meshgrid(X, Y)
    Z = survivors
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, antialiased=True)
    ax.set_xlabel("food supply", fontsize=15)
    ax.set_ylabel("p_cannibalism", fontsize=15)
    ax.set_zlabel("Survived agents", fontsize=15)
    fig.suptitle("Number of alive agents after 1000 time steps", fontsize=20)
    plt.show()


def plot_surface2():
    nr_threads = 12
    food = genfromtxt("food_available_5000_short_0-2.csv", delimiter=",")
    time_steps=food.shape[1]
    p_cannibalise = np.linspace(0, 0.2, nr_threads)
    time_steps = np.arange(time_steps)[2000:]

    fig = plt.figure()
    ax = fig.gca(projection="3d")

    X = time_steps
    Y = p_cannibalise
    X, Y = np.meshgrid(X, Y)
    Z = food[:,2000:]
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, antialiased=True)
    ax.set_xlabel("time steps", fontsize=15)
    ax.set_ylabel("p_cannibalise", fontsize=15)
    ax.set_zlabel("Food available", fontsize=15)
    fig.suptitle("Food available with 12 food sources added each time step", fontsize=20)
    # ------------------------------------------------------
    pop = genfromtxt("population_5000_short_0-2.csv", delimiter=",")
    time_steps = pop.shape[1]
    p_cannibalise = np.linspace(0, 0.2, nr_threads)
    time_steps = np.arange(time_steps)[2000:]

    fig = plt.figure()
    ax = fig.gca(projection="3d")

    X = time_steps
    Y = p_cannibalise
    X, Y = np.meshgrid(X, Y)
    Z = pop[:,2000:]
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, antialiased=True)
    ax.set_xlabel("time steps", fontsize=15)
    ax.set_ylabel("p_cannibalise", fontsize=15)
    ax.set_zlabel("Population size", fontsize=15)
    fig.suptitle("Population size during simulation with 12 food sources each time step", fontsize=20)
    #-----------------------------------------------------
    fig = plt.figure()
    ax = fig.gca(projection="3d")

    X = time_steps
    Y = p_cannibalise
    X, Y = np.meshgrid(X, Y)
    Z = food[:,2000:]/pop[:,2000:]
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, antialiased=True)
    ax.set_xlabel("time steps", fontsize=15)
    ax.set_ylabel("p_cannibalise", fontsize=15)
    ax.set_zlabel("food per individual", fontsize=15)
    fig.suptitle("Food per individual during simulation with 12 new food sources each time step", fontsize=20)
    plt.show()

def plot_surface3():
    nr_threads = 12
    food = genfromtxt("food_available_10000_double_half.csv", delimiter=",")
    time_steps=food.shape[1]
    p_cannibalise = np.linspace(0, 0.5, nr_threads)
    time_steps = np.arange(time_steps)
    subpic = [0, 1, 2, 6, 9, 11]
    fig = plt.figure()

    X = time_steps
    Y = p_cannibalise
    Z = food
    for pic in subpic:
        plt.plot(X, Z[pic, :], label="p_cannibalise={:.3f}".format(p_cannibalise[pic]))
    plt.xlabel("time steps")
    plt.ylabel("Food available")
    plt.legend()
    plt.title("Food available with 5 new food sources each time step.\n Lowered to 2 after 5000 time steps \n and 1 after 7500 time steps")
    # ------------------------------------------------------
    pop = genfromtxt("population_10000_double_half.csv", delimiter=",")
    time_steps = pop.shape[1]
    p_cannibalise = np.linspace(0, 0.5, nr_threads)
    time_steps = np.arange(time_steps)

    fig = plt.figure()

    X = time_steps
    Y = p_cannibalise
    Z = pop
    for pic in subpic:
        plt.plot(X, Z[pic, :], label="p_cannibalise={:.3f}".format(p_cannibalise[pic]))
    plt.xlabel("time steps")
    plt.ylabel("Population size")
    plt.title("Food available with 5 new food sources each time step.\n Lowered to 2 after 5000 time steps \n and 1 after 7500 time steps")
    plt.legend()
    #-----------------------------------------------------
    fig = plt.figure()

    X = time_steps
    Y = p_cannibalise
    Z = food/pop
    for pic in subpic:
        plt.plot(X, Z[pic, :], label="p_cannibalise={:.3f}".format(p_cannibalise[pic]))
    plt.xlabel("time steps")
    plt.ylabel("food per individual")
    plt.legend()
    plt.title("Food available with 5 new food sources each time step.\n Lowered to 2 after 5000 time steps \n and 1 after 7500 time steps")
    plt.show()