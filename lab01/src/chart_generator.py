import matplotlib.pyplot as plt
from utils_numba import FOLDER
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 16
plt.rcParams.update({'legend.fontsize': 'large'})


def chart_generator(x_list, y_list, title, legend, filename):

    plt.ylabel(r"$\it{y}(t)$")
    plt.xlabel(r"$\it{t}(s)$")
    plt.title(title)
    figure = plt.gcf()
    figure.set_size_inches(12, 8)
    for i, (x, y) in enumerate(zip(x_list, y_list)):
        plt.plot(x, y)

    plt.gca().legend(legend)
    plt.savefig(FOLDER+filename)
    plt.close()


def chart_err(x_list, y_list, title, legend, filename):

    fig, ax1 = plt.subplots()
    fig.set_size_inches(12, 5)
    left, bottom, width, height = [0.3, 0.36, 0.2, 0.2]
    ax2 = fig.add_axes([left, bottom, width, height])
    ax1.set_xlabel(r"$\it{t}(s)$")
    ax1.set_ylabel(r"$\it{y_{num}}(t)-\it{y_{dok}(t)}$")
    ax1.set_title(title)
    ax2.set_ylim([0, 1e-3])

    for x, y in zip(x_list, y_list):
        ax1.plot(x, y)

    for x, y in zip(x_list[:-1], y_list[:-1]):
        ax2.plot(x, y)

    ax1.legend(legend)
    plt.savefig(FOLDER+filename)
    plt.close()


def chart_err_euler(x_list, y_list, title, legend, filename):
    plt.ylabel(r"$\it{y_{num}}(t)-\it{y_{dok}(t)}$")
    plt.xlabel(r"$\it{t}(s)$")
    plt.title(title)
    figure = plt.gcf()
    figure.set_size_inches(12, 8)

    for x, y in zip(x_list, y_list):
        plt.plot(x, y)

    plt.legend(legend)
    plt.savefig(FOLDER+filename)
    plt.close()


def rlc_chart_generator(time, datas, titles, legend, filenames, y_labels):

    for title, filename, y_label, data in zip(titles, filenames, y_labels, datas):

        plt.xlabel(r"$\it{t}(s)$")
        plt.ylabel(y_label)
        plt.title(title)
        figure = plt.gcf()
        figure.set_size_inches(12, 5)
        for t, data_row in zip(time, data):
            plt.plot(t, data_row)
        plt.legend(legend)
        plt.savefig(FOLDER+filename)
        plt.close()
