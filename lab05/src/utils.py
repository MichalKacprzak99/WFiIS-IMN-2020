import os
from math import sin, pi

N_X = 128
N_Y = 128
DELTA = 0.2
MAX_X = DELTA * N_X
MAX_Y = DELTA * N_Y
TOL = 1e-8
k = 16
FOLDER = '../images/'


def list_gen(num):
    return [[] for _ in range(num)]


def create_images_folder():
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)


def warunki_dirichleta(V):
    for i in range(N_Y + 1):
        V[0][i] = sin(pi * DELTA * i / MAX_Y)
        V[N_X][i] = sin(pi * DELTA * i / MAX_Y)

    for i in range(N_X + 1):
        V[i][N_Y] = -1.0 * sin(2 * pi * DELTA * i / MAX_X)
        V[i][0] = sin(2 * pi * DELTA * i / MAX_X)
