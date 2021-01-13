from chart_generator import chart_generator
from utils_numba import g, time_looping


def count_by_trapez(x, v, delta_t, alpha):
    delta = 1e-10

    x_next = x
    v_next = v

    while True:
        F = x_next - x - (delta_t / 2.0) * (v + v_next)
        G = v_next - v - (delta_t / 2.0) * (g(alpha, x, v) + g(alpha, x_next, v_next))
        a = [[1.0, -delta_t / 2.0], [(-delta_t / 2.0) * (-2.0 * alpha * x_next * v_next - 1.0), 1.0 - (delta_t / 2.0) *
                                     alpha * (1.0 - pow(x_next, 2.0))]]

        denominator = a[0][0] * a[1][1] - a[0][1] * a[1][0]

        delta_x = (-F * a[1][1] - (-G) * a[0][1]) / denominator
        delta_v = (a[0][0] * (-G) - a[1][0] * (-F)) / denominator

        x_next += delta_x
        v_next += delta_v

        if delta_x < delta and delta_v < delta:
            break

    return x_next, v_next


def trapez():
    x_arr, v_arr, t_arr, delta_t_arr = time_looping(count_by_trapez)
    legend = [r"TOL = $10^{-2}$", r"TOL = $10^{-5}$"]
    title = "metoda trapezow"

    chart_generator(t_arr, x_arr, title, legend, r"$\it{t}(s)$", r"$\it{x}(t)$", 'metoda_trapezow_x_t.png')
    chart_generator(t_arr, v_arr, title, legend, r"$\it{t}(s)$", r"$\it{v}(t)$", 'metoda_trapezow_v_t.png')
    chart_generator(t_arr, delta_t_arr, title, legend, r"$\it{t}(s)$", r"$\it{dt}(t)$", 'metoda_trapezow_dt_t.png')
    chart_generator(x_arr, v_arr, title, legend, r"$\it{x}$", r"$\it{v}$",'metoda_trapezow_v_x.png')
