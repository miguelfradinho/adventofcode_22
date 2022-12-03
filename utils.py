import os
from os import path


def get_file(exercise, ext="txt"):
    file_name = f"input_{exercise}.{ext}"
    return open(path.join(os.getcwd(), "sol_snake", file_name), "r", encoding="utf-8")
