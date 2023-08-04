import os
import cv2
from typing import BinaryIO



def get_next_filename(folder_path:str):

    files = os.listdir(folder_path)

    if len(files)== 0:
        return 0

    max_file_number = max([int(file.split(".")[0]) for file in files])

    return max_file_number + 1




def save_image_file_to_user(image, path:str):

    image_name = get_next_filename(path)

    image_path = os.path.join(path, f"{image_name}.jpg")

    cv2.imwrite(image_path, image)
