from utils import N_Y, N_X, DELTA, TOL, MAX_Y, MAX_X
import numpy as np
from chart_generator import map_generator
from math import exp


def value_c_alpha(alpha, k):
    if alpha == k // 2 or alpha == -k // 2:
        return 0.5
    else:
        return 1.0


def c_alpha_beta(alpha, beta, k):
    return value_c_alpha(alpha, k) * value_c_alpha(beta, k)


def gestosc_ladunku(x, y):
    sigma_x = 0.1 * MAX_X
    sigma_y = 0.1 * MAX_Y
    return 0.1 * exp(-pow((x - 0.5 * MAX_X) / sigma_x, 2) - pow((y - 0.5 * MAX_Y) / sigma_y, 2))


def calkowanie_zrodel(i, j, k):
    zrodlo = 0
    div = 0
    for alpha in range(-k // 2, k // 2 + 1):
        for beta in range(-k // 2, k // 2 + 1):
            zrodlo += c_alpha_beta(alpha, beta, k) * gestosc_ladunku((i + alpha) * DELTA, (j + beta) * DELTA)
            div += c_alpha_beta(alpha, beta, k)

    return zrodlo / div


def fill_V(k, V):
    for i in range(k, N_X, k):
        for j in range(k, N_Y, k):
            V[i][j] = 0.25 * (V[i + k][j] + V[i - k][j] + V[i][j + k] + V[i][j - k] +
                              pow(DELTA * k, 2) * calkowanie_zrodel(i, j, k))


def calka_funkcjonalna(k, V):
    result = 0.0
    for i in range(0, N_X, k):
        for j in range(0, N_Y, k):
            div = DELTA * 2 * k
            first = pow(((V[i + k][j] - V[i][j]) / div + (V[i + k][j + k] - V[i][j + k]) / div), 2)
            second = pow(((V[i][j + k] - V[i][j]) / div + (V[i + k][j + k] - V[i + k][j]) / div), 2)
            result += pow(k * DELTA, 2) * (first / 2 + second / 2 - calkowanie_zrodel(i, j, k) * V[i][j])

    return result


def operation_V(k, V):
    for i in range(0, N_X, k):
        for j in range(0, N_Y, k):
            k_2 = k // 2
            V[i + k_2][j + k_2] = 0.25 * (V[i][j] + V[i + k][j] + V[i][j + k] + V[i + k][j + k])
            V[i + k][j + k_2] = 0.5 * (V[i + k][j] + V[i + k][j + k])
            V[i + k_2][j + k] = 0.5 * (V[i][j + k] + V[i + k][j + k])
            V[i + k_2][j] = 0.5 * (V[i][j] + V[i + k][j])
            V[i][j + k_2] = 0.5 * (V[i][j] + V[i][j + k])


def V_for_chart(k, V, V_tmp):
    for i in range(0, N_X, k):
        for j in range(0, N_Y, k):
            i_x = int(i / k)
            j_y = int(j / k)
            V_tmp[i_x][j_y] = V[i][j]


def relaksacja_wielosiatkowa(k, V):
    it = 0
    S = []
    S_prev = calka_funkcjonalna(k, V)
    while True:
        if it == 0:
            pass
        else:
            S_prev = S[-1]
        fill_V(k, V)
        S.append(calka_funkcjonalna(k, V))
        it += 1
        if abs((S[-1] - S_prev) / S_prev) < TOL:
            break

    size_x = int(N_X / k + 1)
    size_y = int(N_Y / k + 1)
    V_tmp = np.zeros((size_x, size_y))
    V_for_chart(k, V, V_tmp)

    x, y = np.mgrid[0:N_X / 5 + DELTA:DELTA * k, 0:N_Y / 5 + DELTA:DELTA * k]
    map_generator(x, y, V_tmp, rf'Relaksacja wielosiatkowa k={k}', f'wielosiatkowa_V_k_{k}.png')

    if k != 1:
        operation_V(k, V)

    return it, S
