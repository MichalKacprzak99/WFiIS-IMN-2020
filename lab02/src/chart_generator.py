import matplotlib.pyplot as plt
from utils_numba import FOLDER
import numpy as np
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 16
plt.rcParams.update({'legend.fontsize': 'large'})


def chart_generator(x, y, z, title, legend, filename):
    plt.ylabel(r"$\it{u}(t)$, $\it{v}(t)$")
    plt.xlabel(r"$\it{t}(s)$")
    plt.title(title)
    figure = plt.gcf()
    figure.set_size_inches(12, 8)
    plt.plot(x, y)
    plt.plot(x, z)
    plt.xticks(np.arange(0, 101, 10))
    plt.yticks(np.arange(0, 501, 50))
    plt.grid(True)
    plt.gca().legend(legend)
    plt.savefig(FOLDER + filename)
    plt.close()
