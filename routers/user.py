import os
import io
from fastapi import File, Form, Request, UploadFile, APIRouter, status
from database.crud import fetchone_document
from database.schema import Users
from utils.validate import get_object_id, verify_image
from exceptions.custom_execption import BadRequestException, NotFoundException
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
async def add_image(user_id:str =Form(...), image:UploadFile = File(...)):

    image_data = await image.read()

    if not await verify_image(image_data):
        raise BadRequestException("Invalid image or image type")
    

    
    image_data = io.BytesIO(image_data)

    user = await fetchone_document(Users, id=get_object_id(user_id))

    if not user:
        raise NotFoundException("User does not exist")
    
    file_path_for_user = os.path.join(os.getcwd(), f"static/model_data/{user_id}")

    await create_directory_if_not_exists(file_path_for_user)

    image_path = await save_image_file_to_user(image_data, file_path_for_user)

    model_path = os.path.join(os.getcwd(), "model.pkl")

    await update_model(image_path, user, model_path)
            

    return CustomResponse("Added Image To User Successfuly")