import os
import shutil
from typing import BinaryIO



async def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)





async def get_next_filename(folder_path:str):

    files = os.listdir(folder_path)

    if len(files)== 0:
        return 0

    max_file_number = max([int(file.split(".")[0]) for file in files])

    return max_file_number + 1




async def save_image_file_to_user(image:BinaryIO, path:str):

    image_name = await get_next_filename(path)

    image_path = os.path.join(path, f"{image_name}.jpg")

    with open(image_path, "wb") as f:
        shutil.copyfileobj(image, f)

    return image_path
