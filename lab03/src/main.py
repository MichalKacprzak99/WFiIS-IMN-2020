from utils_numba import create_images_folder
from metoda_rk2 import rk2
from metoda_trapezow import trapez
if __name__ == "__main__":
    create_images_folder()
    rk2()
    trapez()