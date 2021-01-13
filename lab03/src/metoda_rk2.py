from chart_generator import chart_generator
from utils_numba import g, time_looping


def count_by_rk2(x, v, delta_t, alpha):
    k1_x = v
    k1_v = g(alpha, x, v)

    k2_x = v + delta_t * k1_v
    k2_v = g(alpha, x + delta_t * k1_x, v + delta_t * k1_v)

    return x + (delta_t / 2.0) * (k1_x + k2_x), v + (delta_t / 2.0) * (k1_v + k2_v)


def rk2():
    x_arr, v_arr, t_arr, delta_t_arr = time_looping(count_by_rk2)
    legend = [r"TOL = $10^{-2}$", r"TOL = $10^{-5}$"]
    title = "metoda RK2"

    chart_generator(t_arr, x_arr, title, legend, r"$\it{t}(s)$", r"$\it{x}(t)$", 'rk2_x_t.png')
    chart_generator(t_arr, v_arr, title, legend, r"$\it{t}(s)$", r"$\it{v}(t)$", 'rk2_v_t.png')
    chart_generator(t_arr, delta_t_arr, title, legend, r"$\it{t}(s)$", r"$\it{dt}(t)$", 'rk2_dt_t.png')
    chart_generator(x_arr, v_arr, title, legend, r"$\it{x}$", r"$\it{v}$",'rk2_v_x.png')