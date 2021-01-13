from math import pow

from numba import njit
import numpy as np
from chart_generator import map_generator, chart_generator
from utils_numba import EPSILON, TOL, V_1, DELTA, N_X, N_Y
from utils_numba import count_stop_condition, WB_von_Neumanna
from utils_numba import first_density, second_density, third_density, fourth_density


@njit
def fill_v_n(V_n, V_s, density):
    for i in range(1, N_X):
        for j in range(1, N_Y):
            V_n[i][j] = 0.25 * (V_s[i + 1][j] + V_s[i - 1][j] + V_s[i][j + 1] + V_s[i][j - 1]
                                + density[i][j] * pow(DELTA, 2) / EPSILON)


@njit
def fill_v_s(omega, V_s, V_n):
    for i in range(N_X + 1):
        for j in range(N_Y + 1):
            V_s[i][j] = (1.0 - omega) * V_s[i][j] + omega * V_n[i][j]


def relaksacja_globalna_numba():
    omegas = (0.6, 1.0)
    params_for_chart = {
        "title": "Relaksacja globalna",
        "legend": [r"$\it{\omega}=0.6$", r"$\it{\omega}=1.0$"],
        "filename": "relaksacja_globalna.png"
    }

    S = [[], []]
    steps = []
    for index, omega in enumerate(omegas):

        density = np.zeros((N_X + 1, N_Y + 1))
        V_s = np.zeros((N_X + 1, N_Y + 1))
        error = np.zeros((N_X + 1, N_Y + 1))
        V_n = np.zeros((N_X + 1, N_Y + 1))
        for i in range(N_X + 1):

            V_s[i][0] = V_1
            V_n[i][0] = V_1
            for j in range(N_Y + 1):
                density[i][j] = first_density(i * DELTA, j * DELTA) + second_density(i * DELTA, j * DELTA) + \
                                third_density(i * DELTA, j * DELTA) + fourth_density(i * DELTA, j * DELTA)
        step = 0

        while True:

            fill_v_n(V_n, V_s, density)

            WB_von_Neumanna(V_n)

            fill_v_s(omega, V_s, V_n)

            S[index].append(count_stop_condition(V_n, density))

            if step > 0 and abs((S[index][step] - S[index][step - 1]) / S[index][step - 1]) < TOL:
                break
            step += 1

        steps.append(step + 1)
        x, y = np.mgrid[0:N_X / 10 + DELTA:DELTA, 0:N_Y / 10 + DELTA:DELTA]

        for i in range(1, N_X):
            for j in range(1, N_Y):
                error[i][j] = ((V_n[i + 1][j] - 2.0 * V_n[i][j] + V_n[i - 1][j]) / pow(DELTA, 2) +
                               (V_n[i][j + 1] - 2.0 * V_n[i][j] + V_n[i][j - 1]) / (pow(DELTA, 2))) + \
                              density[i][j] / EPSILON

        map_generator(x, y, error, rf'Relaksacja globalna błąd $\omega$={omega}', f'{omega}err.png')
        map_generator(x, y, V_n, rf'Relaksacja globalna V(x,y) $\omega$={omega}', f'{omega}_v.png')

    chart_generator(steps, S, **params_for_chart)
