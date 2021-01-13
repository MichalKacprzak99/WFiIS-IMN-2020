import math
import os

FOLDER = 'images/'


def create_images_folder():
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)


def euler_dok(x, c):
    return math.exp(x * c)


def analytical_solution(t_max, t_min, time_step, param_lambda):
    n = int((t_max - t_min) // time_step)
    x, y = [[] for _ in range(2)]

    for i in range(n):
        x_n = i * time_step
        y_n = euler_dok(x_n, param_lambda)
        x.append(x_n)
        y.append(y_n)

    return x, y


def list_gen(num):
    return [[] for _ in range(num)]