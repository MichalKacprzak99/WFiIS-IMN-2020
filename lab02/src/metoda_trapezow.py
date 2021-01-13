import numpy as np
from utils_numba import f
from chart_generator import chart_generator


def metoda_trapezow():
    params_for_chart = {
        "title": "Metoda Picarda",
        "legend": [r"$\it{u}(t)$", r"$\it{z}(t)$"],
        "filename": 'picard.png',
    }
    beta = 0.001
    N = 500
    gamma = 0.1
    t_max = 100
    dt = 0.1
    TOL = 1e-6
    MI = 20
    n = int(t_max // dt) + 1
    alpha = (beta * N) - gamma

    time = np.linspace(0, n * dt, num=n, endpoint=True)

    picard = np.ones(time.shape)
    newton = np.ones(time.shape)
    z = np.zeros(time.shape)
    z[0] = N - 1.0

    # Picard
    for i in range(1, n):
        u_prev = picard[i - 1]
        u = 0
        for mi in range(MI+1):
            if abs(u - u_prev) < TOL:
                break

            u = picard[i - 1] + (dt / 2.0) * (f(alpha, beta, picard[i - 1]) +
                                              f(alpha, beta, u_prev))

        picard[i] = u
        z[i] = N - picard[i]

    chart_generator(time, picard, z, **params_for_chart)

    # Newton
    for i in range(1, n):
        u_prev = newton[i - 1]
        u = 0

        for mi in range(MI+1):
            if abs(u - u_prev) < TOL:
                break

            u = u_prev - (u_prev - newton[i - 1] - (dt / 2.0) * (f(alpha, beta, newton[i - 1]) +
                                                                 f(alpha, beta, u_prev))) / \
                (1 - (dt / 2.0) * (alpha - 2 * beta * u_prev))

        newton[i] = u
        z[i] = N - newton[i]

    params_for_chart = {
        "title": "Iteracja Newtona",
        "legend": [r"$\it{u}(t)$", r"$\it{z}(t)$"],
        "filename": 'newton.png',
    }
    chart_generator(time, newton, z, **params_for_chart)
