from nav_stokes import nav_stokes
from utils import create_folder
if __name__ == "__main__":
    create_folder('../images/')
    create_folder('../error_data/')
    nav_stokes(-1000)
    nav_stokes(-4000)
    nav_stokes(4000)
