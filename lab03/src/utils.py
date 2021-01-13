import os

FOLDER = 'images/'


def g(alpha, x, v):
    return alpha * (1.0 - pow(x, 2)) * v - x


def create_images_folder():
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)


def list_gen(num):
    return [[] for _ in range(num)]


def time_looping(metoda):
    TOL = [1e-2, 1e-5]

    S = 0.75
    p = 2.0
    T_MAX = 40.0
    ALPHA = 5.0
    delta_t_arr = list_gen(2)
    x_arr = list_gen(2)
    v_arr = list_gen(2)
    t_arr = list_gen(2)
    for i, tol in enumerate(TOL):
        x = 0.01
        v = 0.0
        t = 0.0
        dt = 1.0
        while t < T_MAX:

            step_1 = metoda(x, v, dt, ALPHA)
            step_1 = metoda(step_1[0], step_1[1], dt, ALPHA)

            step_2 = metoda(x, v, 2.0 * dt, ALPHA)

            error_x = (step_2[0] - step_1[0]) / (pow(2, p) - 1.0)
            error_v = (step_2[1] - step_1[1]) / (pow(2, p) - 1.0)

            max_error = max(abs(error_x), abs(error_v))

            if max_error < tol:
                t = t + 2 * dt
                x = step_1[0]
                v = step_1[1]
                t_arr[i].append(t)
                x_arr[i].append(x)
                v_arr[i].append(v)
                delta_t_arr[i].append(dt)

            dt *= pow((S * tol) / max_error, (1.0 / (p + 1.0)))

    return x_arr, v_arr, t_arr, delta_t_arr
