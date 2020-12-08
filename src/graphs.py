import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from PIL import Image
from PIL import ImageTk as itk

class CanvasAnimate:
    def __init__(self, res=500, food_source=0.8, l=5):
        self.l = l
        self.res = res
        self.tk = Tk()
        self.tk.geometry(str(int(res * 1.1)) + 'x' + str(int(res * 1.3)))
        self.tk.configure(background='white')

        self.canvas = Canvas(self.tk, bd=2)  # Generate animation window
        self.tk.attributes('-topmost', 0)
        self.canvas.place(x=res / 20, y=res / 20, height=res, width=res)
        ccolor = ['#0008FF', '#DB0000', '#12F200']

        self.food = Scale(self.tk, from_=0, to=1, orient=HORIZONTAL, label='food source', font=("Helvetica", 8),
                            resolution=0.01)
        self.food.place(relx=.57, rely=.85, relheight=0.12, relwidth=0.33)
        self.food.set(0.9)  # Parameter slider for lightning rate
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

