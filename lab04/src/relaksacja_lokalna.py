from math import pow

import numpy as np
from chart_generator import chart_generator
from utils import EPSILON, TOL, V_1, DELTA, N_X, N_Y
from utils import count_stop_condition, WB_von_Neumanna
from utils import first_density, second_density, third_density, fourth_density


def fill_v_n(V_n, omega, density):
    for i in range(1, N_X):
        for j in range(1, N_Y):
            V_n[i][j] = (1.0 - omega) * V_n[i][j] + (0.25 * omega) * \
                        (V_n[i + 1][j] + V_n[i - 1][j] + V_n[i][j + 1] + V_n[i][j - 1] +
                         (pow(DELTA, 2) / EPSILON) * density[i][j])


def relaksacja_lokalna():
    omegas = (1.0, 1.4, 1.8, 1.9)
    params_for_chart = {
        "title": "Relaksacja lokalna",
        "legend": [r"$\it{u}(t)$", r"$\it{v}(t)$", r"$\it{h}(t)$", r"$\it{t}(t)$"],
        "filename": "relaksacja_lokalna.png"
    }

    S = [[], [], [], []]
    steps = []
    for index, omega in enumerate(omegas):
        density = np.zeros((N_X + 1, N_Y + 1))
        V_n = np.zeros((N_X + 1, N_Y + 1))
        for i in range(N_X + 1):
            V_n[i][0] = V_1
            for j in range(N_Y + 1):
                density[i][j] = first_density(i * DELTA, j * DELTA) + second_density(i * DELTA, j * DELTA) + \
                                third_density(i * DELTA, j * DELTA) + fourth_density(i * DELTA, j * DELTA)

        step = 0

        while True:
            fill_v_n(V_n, omega, density)

            WB_von_Neumanna(V_n)

            S[index].append(count_stop_condition(V_n, density))

            if step > 0 and abs((S[index][step] - S[index][step - 1]) / S[index][step - 1]) < TOL:
                break
            step += 1
        steps.append(step + 1)

    chart_generator(steps, S, **params_for_chart)
