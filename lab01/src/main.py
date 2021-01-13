from euler import euler
from rk4 import rk4
from rk2 import rk2
from rlc import rlc
from utils_numba import create_images_folder


if __name__ == "__main__":
    create_images_folder()
    euler()
    rk2()
    rk4()
    # rlc()
