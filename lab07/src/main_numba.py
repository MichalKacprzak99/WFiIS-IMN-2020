from nav_stokes_numba import nav_stokes_numba
from utils import create_folder
if __name__ == "__main__":
    create_folder('../images/')
    create_folder('../error_data/')
    nav_stokes_numba(-1000)
    nav_stokes_numba(-4000)
    nav_stokes_numba(4000)
