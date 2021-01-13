from utils_numba import list_gen, analytical_solution, euler_dok
from chart_generator import chart_generator, chart_err_euler


def euler():
    params_for_chart = {
        "title": "z1. - Metoda jawna Euler - rozwiązanie",
        "legend": [r"$\it{\Delta t}=0.01$ s", r"$\it{\Delta t}=0.1$ s", r"$\it{\Delta t}=1$ s", "analytical"],
        "filename": 'euler.png',
    }
    param_lambda = -1.0
    t_min = 0
    t_max = 5
    time_steps = [0.01, 0.1, 1.0]

    x = list_gen(4)
    y = list_gen(4)
    y_err = list_gen(3)
    for i, time_step in enumerate(time_steps):
        n = int((t_max - t_min) // time_step)
        y_n = 1
        for j in range(n+1):
            y[i].append(y_n)

            x_n = j * time_step
            x[i].append(x_n)

            y_err[i].append(y_n - euler_dok(x_n, param_lambda))

            y_n = y_n + time_step * param_lambda * y_n

    x[3], y[3] = analytical_solution(t_max, t_min, time_steps[0], param_lambda)

    chart_generator(x, y, **params_for_chart)

    params_for_chart = {
        "title": "z1. - Metoda jawna Euler - błąd globalny",
        "legend": [r"$\it{\Delta t}=0.01$ s", r"$\it{\Delta t}=0.1$ s", r"$\it{\Delta t}=1$ s"],
        "filename": 'euler_err.png',
    }
    chart_err_euler(x, y_err, **params_for_chart)
