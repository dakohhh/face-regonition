import os
import face_recognition
from fastapi import File, Form, Request, UploadFile, APIRouter, status
from database.crud import fetchone_document
from database.schema import Users
from utils.validate_bson import get_object_id
from exceptions.custom_execption import NotFoundException
from models.model import CreateUser
from utils.file_func import create_directory_if_not_exists, save_image_file_to_user
from utils.model_func import update_model
from response.response import CustomResponse




router = APIRouter(tags=["User"], prefix="/user")



@router.get("/")
async def get_users(request:Request):
        
    return CustomResponse("Get User Successfully")


@router.post("/")
async def add_user(request:Request, user:CreateUser):

    new_user = Users(firstname=user.firstname, lastname=user.lastname, matric_no=user.matric_no)

    new_user.save()

    return CustomResponse("Added User Successfully", status=status.HTTP_201_CREATED)



@router.post("/add-image")
async def add_image(user_id:str =Form(...), image: UploadFile = File(...)):

    user = await fetchone_document(Users, id=get_object_id(user_id))

    print(user)

    if not user:
        raise NotFoundException("User does not exist")
    
    file_path_for_user = os.path.join(os.getcwd(), f"static/model_data/{user_id}")

    await create_directory_if_not_exists(file_path_for_user)

    image_path = await save_image_file_to_user(image.file, file_path_for_user)

    model_path = os.path.join(os.getcwd(), "model.pkl")


    
            

    return CustomResponse("Added Image To User Successfuly")