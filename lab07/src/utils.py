import os

FOLDER = '../images/'


def list_gen(num):
    return [[] for _ in range(num)]


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
