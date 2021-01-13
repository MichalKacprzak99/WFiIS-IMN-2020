import math
import os

FOLDER = 'images/'


def create_images_folder():
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)


def f(alpha, beta, x):
    return alpha * x - beta * math.pow(x, 2)
