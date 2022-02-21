# coding: UTF-8

from os import walk, path

from PIL import Image

from . import image


def get_roles() -> str:
    for root, dirs, files in walk("./pic"):
        roles_name = ""
        for _dir in dirs:
            roles_name = roles_name + _dir + "  "
        return roles_name


def get_role_cards(role_name) -> str:
    file_path = f"./pic/{role_name}"
    if not path.exists(file_path):
        return ""
    else:
        img = Image.open(f"{file_path}/combine.png")
        return f"base64://{str(image.image_to_base64(img), encoding='utf-8')}"
