from chart_generator import chart_generator, chart_err
from utils_numba import list_gen, analytical_solution, euler_dok


def rk2():
    params_for_chart = {
        "title": "z2. - Metoda RK2 - rozwiązanie",
        "legend": [r"$\it{\Delta t}=0.01$ s", r"$\it{\Delta t}=0.1$ s", r"$\it{\Delta t}=1$ s", "analytical"],
        "filename": 'rk2.png',
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
            k1 = param_lambda * y_n
            k2 = param_lambda * (y_n + time_step * k1)

            x_n = j * time_step
            x[i].append(x_n)

            y_err[i].append(y_n - euler_dok(x_n, param_lambda))
            y_n = y_n + (time_step / 2.0) * (k1 + k2)

    x[3], y[3] = analytical_solution(t_max, t_min, time_steps[0], param_lambda)

    chart_generator(x, y, **params_for_chart)
    params_for_chart = {
        "title": "z2. - Metoda RK2 - błąd globalny",
        "legend": [r"$\it{\Delta t}=0.01$ s", r"$\it{\Delta t}=0.1$ s", r"$\it{\Delta t}=1$ s"],
        "filename": 'rk2_err.png',
    }
    chart_err(x, y_err, **params_for_chart)
