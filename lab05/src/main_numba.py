import numpy as np
from chart_generator import chart_generator
from relaksacja_wielosiatkowa_numba import relaksacja_wielosiatkowa_numba
from utils import create_images_folder, warunki_dirichleta
from utils import N_Y, N_X, k

if __name__ == "__main__":
    create_images_folder()
    params_for_chart = {
        "title": r"Wykres zmian $S^{(k)}(it)$",
        "legend": ["k=16", "k=8", "k=4", "k=2", "k=1"],
        "filename": "wielosiatkowa_s.png"
    }

    V = np.zeros((N_X + 1, N_Y + 1))
    iteracje = []
    S = []
    warunki_dirichleta(V)

    while k >= 1:
        it, s = relaksacja_wielosiatkowa_numba(k, V)
        iteracje.append(it)
        S.append(s)
        k //= 2
    chart_generator(iteracje, S, **params_for_chart)
