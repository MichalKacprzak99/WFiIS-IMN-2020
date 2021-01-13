import os
from math import exp

from numba import njit

FOLDER = 'images/'

TOL = 1e-8
EPSILON = 1.0
DELTA = 0.1
N_X = 150
N_Y = 100
V_1 = 10.0
X_MAX = DELTA * N_X
Y_MAX = DELTA * N_Y
SIGMA_X = 0.1 * X_MAX
SIGMA_Y = 0.1 * Y_MAX


def create_images_folder():
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)


@njit
def first_density(x, y):
    return 2.0 * exp((-pow(x - 0.35 * X_MAX, 2) / pow(SIGMA_X, 2)) - (pow(y - 0.25 * Y_MAX, 2) / pow(SIGMA_Y, 2)))


@njit
def second_density(x, y):
    return -2.0 * exp((-pow(x - 0.65 * X_MAX, 2) / pow(SIGMA_X, 2)) - (pow(y - 0.25 * Y_MAX, 2) / pow(SIGMA_Y, 2)))


@njit
def third_density(x, y):
    return -1.0 * exp((-pow(x - 0.35 * X_MAX, 2) / pow(SIGMA_X, 2)) - (pow(y - 0.75 * Y_MAX, 2) / pow(SIGMA_Y, 2)))


@njit
def fourth_density(x, y):
    return 1.0 * exp((-pow(x - 0.65 * X_MAX, 2) / pow(SIGMA_X, 2)) - (pow(y - 0.75 * Y_MAX, 2) / pow(SIGMA_Y, 2)))


@njit
def count_stop_condition(V_n, density):
    s = 0.0

    for i in range(N_X):
        for j in range(N_Y):
            s += pow(DELTA, 2) * (0.5 * pow((V_n[i + 1][j] - V_n[i][j]) / DELTA, 2) + 0.5 * pow(
                (V_n[i][j + 1] - V_n[i][j]) / DELTA, 2) - density[i][j] * V_n[i][j])

    return s


@njit
def WB_von_Neumanna(V_n):
    for i in range(1, N_Y + 1):
        V_n[0][i] = V_n[1][i]
        V_n[N_X][i] = V_n[N_X - 1][i]
