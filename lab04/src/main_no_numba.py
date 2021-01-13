from utils import create_images_folder
from relaksacja_globalna import relaksacja_globalna
from relaksacja_lokalna import relaksacja_lokalna


if __name__ == "__main__":
    print("Szacunkowy czas wykonywania się programu bez biblioteki numba to około 2 godziny\n"
          "W celi sprawdzenia działania programu zalecam uruchomienie komendą make run\n"
          "jednak wymaga to wcześniejszego zainstalowania biblioteki numba")
    create_images_folder()
    relaksacja_globalna()
    relaksacja_lokalna()

