import matplotlib.pyplot as plt
from utils_numba import FOLDER

plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 16
plt.rcParams.update({'legend.fontsize': 'large'})


def chart_generator(x_set, y_set, title, legend, x_label, y_label, filename):
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.title(title)
    figure = plt.gcf()
    figure.set_size_inches(12, 8)
    for x, y in zip(x_set, y_set):
        plt.plot(x, y)

    plt.gca().legend(legend)
    plt.savefig(FOLDER + filename)
    plt.close()
