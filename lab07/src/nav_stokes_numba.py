from numba import njit
import numpy as np
from chart_generator import map_generator, contour_generator

DELTA = 0.01
p = 1.0
mi = 1.0
N_X = 200
N_Y = 90
i1 = 50
j1 = 55
j2 = j1 + 2
IT_MAX = 20000


@njit
def y(i):
    return DELTA * i


@njit
def x(i):
    return DELTA * i


@njit
def psi_A(psi, Qwe):
    for j in range(j1, N_Y + 1):
        psi[0][j] = Qwe / (2 * mi) * (pow(y(j), 3) / 3 - pow(y(j), 2) / 2 * (y(j1) + y(N_Y)) + y(j) * y(
            j1) * y(N_Y))


@njit
def psi_C(psi, Qwy, Qwe):
    for j in range(0, N_Y + 1):
        psi[N_X][j] = Qwy / (2 * mi) * (y(j) * y(j) * y(j) / 3 - y(j) * y(j) / 2 * y(N_Y)) + Qwe * y(j1) * y(
            j1) * (-y(j1) + 3 * y(N_Y)) / (12 * mi)


@njit
def psi_B(psi):
    for i in range(1, N_X):
        psi[i][N_Y] = psi[0][N_Y]


@njit
def psi_D(psi):
    for i in range(i1, N_X):
        psi[i][0] = psi[0][j1]


@njit
def psi_E(psi):
    for j in range(1, j1 + 1):
        psi[i1][j] = psi[0][j1]


@njit
def psi_F(psi):
    for i in range(1, i1 + 1):
        psi[i][j1] = psi[0][j1]


@njit
def modify_psi(psi, Qwe, Qwy):

    psi_A(psi, Qwe)
    psi_C(psi, Qwy, Qwe)
    psi_B(psi)
    psi_D(psi)
    psi_E(psi)
    psi_F(psi)


@njit
def new_psi_i_j(i, j, psi, zeta):
    return 0.25 * (psi[i + 1][j] + psi[i - 1][j] + psi[i][j + 1] + psi[i][j - 1] - DELTA * DELTA * zeta[i][j])


@njit
def zeta_A(zeta, Qwe):
    for j in range(j1, N_Y + 1):
        zeta[0][j] = Qwe / (2 * mi) * (2 * y(j) - y(j1) - y(N_Y))


@njit
def zeta_C(zeta, Qwe):
    for j in range(0, N_Y + 1):
        zeta[N_X][j] = Qwe / (2 * mi) * (2 * y(j) - y(N_Y))


@njit
def zeta_B(zeta, psi):
    for i in range(1, N_X):
        zeta[i][N_Y] = 2.0 / (DELTA * DELTA) * (psi[i][N_Y - 1] - psi[i][N_Y])


@njit
def zeta_D(zeta, psi):
    for i in range(i1 + 1, N_X):
        zeta[i][0] = 2.0 / (DELTA * DELTA) * (psi[i][1] - psi[i][0])


@njit
def zeta_E(zeta, psi):
    for j in range(1, j1):
        zeta[i1][j] = 2.0 / (DELTA * DELTA) * (psi[i1 + 1][j] - psi[i1][j])


@njit
def zeta_F(zeta, psi):
    for i in range(1, i1 + 1):
        zeta[i][j1] = 2.0 / (DELTA * DELTA) * (psi[i][j1 + 1] - psi[i][j1])

    zeta[i1][j1] = 0.5 * (zeta[i1 - 1][j1] + zeta[i1][j1 - 1])


@njit
def modify_zeta(Qwe, Qwy, psi, zeta):
    zeta_A(zeta, Qwe)
    zeta_C(zeta, Qwy)
    zeta_B(zeta, psi)
    zeta_D(zeta, psi)
    zeta_E(zeta, psi)
    zeta_F(zeta, psi)


@njit
def new_zeta_i_j(omega, i, j, zeta, psi):
    return 0.25 * (zeta[i + 1][j] + zeta[i - 1][j] + zeta[i][j + 1] + zeta[i][j - 1]) - omega * p / (16 * mi) * \
           ((psi[i][j + 1] - psi[i][j - 1]) * (zeta[i + 1][j] - zeta[i - 1][j]) - (psi[i + 1][j] - psi[i - 1][j]) *
            (zeta[i][j + 1] - zeta[i][j - 1]))


@njit
def calculate_u_v(psi, u, v):
    for i in range(1, N_X):
        for j in range(1, N_Y):
            if (i > i1 or j > j1):
            # if i > i1 or j > j1:
                u[i][j] = (psi[i][j + 1] - psi[i][j - 1]) / (2 * DELTA)
                v[i][j] = -(psi[i + 1][j] - psi[i - 1][j]) / (2 * DELTA)


@njit
def error(zeta, psi):
    result = 0.0
    for i in range(1, N_X):
        result += psi[i+1][j2] + psi[i-1][j2] + psi[i][j2+1] + psi[i][j2-1] - 4*psi[i][j2] - DELTA*DELTA*zeta[i][j2]
    return result


@njit
def solve(psi, zeta, Qwe, Qwy):
    errors = []
    for it in range(1, IT_MAX + 1):
        if it < 2000:
            omega = 0.0
        else:
            omega = 1.0
        for i in range(1, N_X):
            for j in range(1, N_Y):
                if (i <= i1 and j > j1) or (i > i1):
                # if i > i1 or j > j1:
                    psi[i][j] = new_psi_i_j(i, j, psi, zeta)
                    zeta[i][j] = new_zeta_i_j(omega, i, j, zeta, psi)

        modify_zeta(Qwe, Qwy, psi, zeta)
        errors.append(error(zeta, psi))
    return errors


def nav_stokes_numba(Qwe):
    Qwy = Qwe * (pow(y(N_Y), 3) - pow(y(j1), 3) - 3 *
                 pow(y(N_Y), 2) * y(j1) + 3 * pow(y(j1), 2) *
                 y(N_Y)) / (pow(y(N_Y), 3))

    psi = np.zeros((N_X + 1, N_Y + 1))
    zeta = np.zeros((N_X + 1, N_Y + 1))
    psi[0:i1, 0:j1] = np.nan
    zeta[0:i1, 0:j1] = np.nan
    modify_psi(psi, Qwe, Qwy)
    # modify_zeta(Qwe, Qwy, psi, zeta)

    errors = solve(psi, zeta, Qwe, Qwy)
    with open(f'../error_data/errors_{Qwe}.txt', 'w') as f:
        for err in errors:
            f.write(f"{err}\n")

    u = np.zeros((N_X + 1, N_Y + 1))
    v = np.zeros((N_X + 1, N_Y + 1))

    calculate_u_v(psi, u, v)

    # tmp_x, tmp_y = np.mgrid[0:N_X / 100 + DELTA:DELTA, 0:N_Y / 100 + DELTA:DELTA]
    tmp_x = np.linspace(0.0, (N_X+1)*DELTA, N_X+1, endpoint=True)
    tmp_y = np.linspace(0.0, (N_Y+1)*DELTA, N_Y+1, endpoint=True)
    map_generator(tmp_x, tmp_y, np.transpose(u), rf'Q={Qwe}, u(x,y)', f'u_{Qwe}.png')
    map_generator(tmp_x, tmp_y, np.transpose(v), rf'Q={Qwe}, v(x,y)', f'v_{Qwe}.png')
    contour_generator(tmp_x, tmp_y, np.transpose(zeta), rf'Q={Qwe}, $\zeta(x,y)$', f'zeta_{Qwe}.png')
    contour_generator(tmp_x, tmp_y, np.transpose(psi), rf'Q={Qwe}, $\psi(x,y)$', f'psi_{Qwe}.png')

