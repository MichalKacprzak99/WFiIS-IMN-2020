from utils import create_images_folder
from relaksacja_globalna_numba import relaksacja_globalna_numba
from relaksacja_lokalna_numba import relaksacja_lokalna_numba


if __name__ == "__main__":
    create_images_folder()
    relaksacja_globalna_numba()
    relaksacja_lokalna_numba()

