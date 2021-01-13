import matplotlib.pyplot as plt
from utils import FOLDER
import numpy as np

plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 16
plt.rcParams.update({'legend.fontsize': 'large'})


def map_generator(x, y, z, title, filename):
    plt.ylabel("y")
    plt.xlabel("x")
    plt.title(title)
    figure = plt.gcf()

    figure.set_size_inches(12, 8)
    z = z[:-1, :-1]
    z_min, z_max = np.amin(z), np.amax(z)
    plt.pcolor(x, y, z, cmap='inferno', vmin=z_min, vmax=z_max)
    plt.colorbar()
    plt.savefig(FOLDER + filename)
    plt.close()


def contour_generator(x, y, z, title, filename):
    plt.ylabel("y")
    plt.xlabel("x")
    plt.title(title+f" liczba konturów wynosi {40}")
    figure = plt.gcf()

    figure.set_size_inches(12, 8)
    z_min, z_max = np.amin(z), np.amax(z)
    plt.contour(x, y, z, cmap='cividis', vmin=z_min, vmax=z_max, levels=50)
    plt.colorbar()
    plt.savefig(FOLDER + filename)
    plt.close()