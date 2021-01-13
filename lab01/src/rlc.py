import math
from chart_generator import rlc_chart_generator


def volt(t, omega):
    return 10.0 * math.sin(t * omega)


def rlc():
    params_for_chart = {
        "titles": ["z4. - Metoda RK4 - I(t)", "z4. - Metoda RK4 - Q(t)"],
        "legend": [r"0.5 $\omega_0$", r"0.8 $\omega_0$", r"1.0 $\omega_0$", r"1.2 $\omega_0$"],
        "filenames": ['rlc_i.png', 'rlc_q'],
        "y_labels": [r'$\it{I}$(t)', r'$\it{Q}$(t)']
    }
    time_step = 1e-4
    R = 100.0
    L = 0.1
    C = 0.001
    w_0 = 1.0 / math.sqrt(L * C)
    T_0 = (2.0 * math.pi) / w_0
    t_min = 0.0
    t_max = 4.0 * T_0
    omega_sources = [0.5 * w_0, 0.8 * w_0, w_0, 1.2 * w_0]

    def list_gen(num):
        return [[] for _ in range(num)]

    Q, I, time = [list_gen(4) for _ in range(3)]
    n = int((t_max - t_min) // time_step)

    for i, omega in enumerate(omega_sources):

        Q_tmp = 0
        I_tmp = 0

        for j in range(n):

            time_tmp = j * time_step
            time_half = (j + 0.5) * time_step
            time_next = (j + 1.0) * time_step

            v = volt(time_tmp, omega)
            v_half = volt(time_half, omega)
            v_next = volt(time_next, omega)

            Q[i].append(Q_tmp)
            I[i].append(I_tmp)
            time[i].append(time_tmp)

            k1Q = I_tmp
            k1I = (v / L) - ((1.0 / (L * C)) * Q_tmp) - ((R / L) * I_tmp)

            k2Q = I_tmp + ((time_step / 2.0) * k1I)
            k2I = (v_half / L) - ((1.0 / (L * C)) * (Q_tmp + (time_step / 2.0) * k1Q)) - \
                  ((R / L) * (I_tmp + (time_step / 2.0) * k1I))

            k3Q = I_tmp + (time_step / 2.0) * k2I
            k3I = (v_half / L) - ((1.0 / (L * C)) * (Q_tmp + (time_step / 2.0) * k2Q)) - \
                  ((R / L) * (I_tmp + (time_step / 2.0) * k2I))

            k4Q = I_tmp + (time_step * k3I)
            k4I = (v_next / L) - (1 / (L * C)) * (Q_tmp + time_step * k3Q) - \
                  ((R / L) * (I_tmp + (time_step * k3I)))

            Q_tmp = Q_tmp + (time_step / 6.0) * (k1Q + 2 * k2Q + 2 * k3Q + k4Q)
            I_tmp = I_tmp + (time_step / 6.0) * (k1I + 2 * k2I + 2 * k3I + k4I)

    rlc_chart_generator(time, [I, Q], **params_for_chart)
