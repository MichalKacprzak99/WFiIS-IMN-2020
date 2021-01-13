from utils_numba import create_images_folder
from metoda_trapezow import metoda_trapezow
from metoda_rk2 import rk2


if __name__ == "__main__":
    create_images_folder()
    metoda_trapezow()
    rk2()
