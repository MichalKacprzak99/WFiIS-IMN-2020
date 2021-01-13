import matplotlib.pyplot as plt
from utils import FOLDER
import numpy as np

plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 16
plt.rcParams.update({'legend.fontsize': 'large'})


def chart_generator(x_set, y_set, title, legend, filename):
    plt.ylabel("S")
    plt.xlabel("it")
    plt.title(title)
    plt.xscale('log')
    figure = plt.gcf()
    figure.set_size_inches(12, 8)
    for x, y in zip(x_set, y_set):
        x = [i for i in range(1, x+1)]
        plt.plot(x, y)
    # plt.plot(x_set, y_set)

    plt.gca().legend(legend)
    plt.savefig(FOLDER + filename)
    plt.close()


def map_generator(x, y, z, title, filename):
    plt.ylabel("y")
    plt.xlabel("x")
    plt.title(title)
    figure = plt.gcf()

    figure.set_size_inches(12, 8)
    z = z[:-1, :-1]
    z_min, z_max = np.amin(z), np.amax(z)
    plt.pcolor(x, y, z, cmap='hot', vmin=z_min, vmax=z_max)
    plt.colorbar()
    plt.savefig(FOLDER + filename)
    plt.close()
