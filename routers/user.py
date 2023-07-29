import os
import face_recognition
from typing import List
from fastapi import File, Form, Request, UploadFile, APIRouter
from database.crud import fetchone_document
from database.schema import Users
from exceptions.custom_execption import NotFoundException
from models.model import CreateUser
from utils.file_func import create_directory_if_not_exists, save_image_file_to_user
from response.response import CustomResponse




router = APIRouter(tags=["User"], prefix="/user")

@router.post("/create")
async def add_user(request:Request, user:CreateUser,  images: List[UploadFile] = File(...)):

    new_user = Users(firstname=user.firstname, lastname=user.lastname, matric_no=user.matric_no)

    new_user.save()

    return CustomResponse("Added User Successfully")



@router.post("/add-image")
async def add_image(user_id:str =Form(...), image: UploadFile = File(...)):

    user = fetchone_document(Users, id=user_id)

    if not user:
        raise NotFoundException("User does not exist")
    
    file_path_for_user = os.path.join(os.getcwd(), f"static/model_data/{user_id}")

    await create_directory_if_not_exists(file_path_for_user)

    image_path = await save_image_file_to_user(image.file, file_path_for_user)

    loaded_image = face_recognition.load_image_file(image_path)
    
    print(type(loaded_image))

    return CustomResponse("Added Image To User Successfuly")