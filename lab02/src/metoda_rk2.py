import numpy as np
import math
from utils_numba import f
from chart_generator import chart_generator


def rk2():
    params_for_chart = {
        "title": "Niejawna metoda RK2",
        "legend": [r"$\it{u}(t)$", r"$\it{v}(t)$"],
        "filename": 'rk2.png',
    }
    beta = 0.001
    N = 500
    gamma = 0.1
    t_max = 100
    delta_t = 0.1
    TOL = 1e-6
    MI = 20
    ITERATIONS = int(t_max / delta_t)
    alpha = (beta * N) - gamma

    a = np.array([[0.25, 0.25 - (math.sqrt(3) / 6.0)], [0.25 + (math.sqrt(3) / 6.0), 0.25]])
    b = np.array([0.5, 0.5])
    c = np.array([0.5 - (math.sqrt(3) / 6.0), 0.5 + (math.sqrt(3) / 6.0)])

    def f1(U1, U2, u):
        return U1 - u - (delta_t * (a[0][0] * f(alpha, beta, U1) + a[0][1] * f(alpha, beta, U2)))

    def f2(U1, U2, u):
        return U2 - u - (delta_t * (a[1][0] * f(alpha, beta, U1) + a[1][1] * f(alpha, beta, U2)))

    def m_value(i, j, u):
        res = (-delta_t) * a[i][j] * (alpha - 2.0 * beta * u)
        if i == j:
            res += 1.0

        return res

    time = np.linspace(0, ITERATIONS * delta_t, num=ITERATIONS + 1, endpoint=True)

    U = np.ones(time.shape)
    z = np.zeros(time.shape)
    z[0] = N - 1.0

    for i in range(1, ITERATIONS + 1):
        U_pre = U1 = U2 = U[i - 1]

        for mi in range(MI+1):

            m = np.array([[m_value(0, 0, U1), m_value(0, 1, U2)],
                          [m_value(1, 0, U1), m_value(1, 1, U2)]])

            F1 = f1(U1, U2, U[i - 1])
            F2 = f2(U1, U2, U[i - 1])

            denominator = (m[0][0] * m[1][1]) - (m[0][1] * m[1][0])
            d_U1 = ((F2 * m[0][1]) - (F1 * m[1][1])) / denominator
            d_U2 = ((F1 * m[1][0]) - (F2 * m[0][0])) / denominator

            U1 += d_U1
            U2 += d_U2

            U_akt = U[i-1] + delta_t * (b[0] * f(alpha, beta, U1) + b[1] * f(alpha, beta, U2))

            if abs(U_akt-U_pre) < TOL:
                break
            U_pre = U_akt
        U[i] = U_akt
        z[i] = N - U[i]

    chart_generator(time, U, z, **params_for_chart)
