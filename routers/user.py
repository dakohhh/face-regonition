import os
import io
import cv2
import asyncio
import face_recognition
from fastapi import File, Form, Request, UploadFile, APIRouter, status
from fastapi.templating import Jinja2Templates
from database.crud import fetchone_document, fetchall
from database.schema import Users
from utils.validate import get_object_id, verify_image
from exceptions.custom_execption import BadRequestException, NotFoundException
from models.model import CreateUser
from utils.file_func import save_image_file_to_user
from utils.model_func import train_evaluate_update, get_class_dict
from response.response import CustomResponse


router = APIRouter(tags=["User"], prefix="/user")


templates = Jinja2Templates(directory="templates")




@router.get("/")
async def get_users(request:Request):

    get_user_task = asyncio.create_task(fetchall(Users))

    class_list = asyncio.create_task(get_class_dict())

    users = [user.to_dict() for user in await get_user_task]

    class_list = await class_list
    
    needs_train = False

    if len(users) > len(class_list):
    
        needs_train = True

    print(needs_train)
    
    
    context = {"request":request, "users":users, "needs_train": needs_train}
        
    return templates.TemplateResponse("view.html", context)


@router.post("/")
async def add_user(request:Request, user:CreateUser):

    new_user = Users(firstname=user.firstname, lastname=user.lastname, matric_no=user.matric_no)

    new_user.save()

    return CustomResponse("Added User Successfully", status=status.HTTP_201_CREATED)




@router.patch("/blacklist/{user_id}")
async def blacklist_user(request:Request, user_id:str):
    user = await fetchone_document(Users, id=get_object_id(user_id))

    user.is_blacklisted = True

    user.save()

    return CustomResponse("Blacklisted User Successfully", status=status.HTTP_200_OK)




@router.patch("/unblacklist/{user_id}")
async def unblacklist_user(request:Request, user_id:str):
    user = await fetchone_document(Users, id=get_object_id(user_id))

    user.is_blacklisted = False

    user.save()

    return CustomResponse("Unblacklisted User Successfully", status=status.HTTP_200_OK)
    


@router.post("/add-image")
async def add_image(user_id:str =Form(...), image:UploadFile = File(...)):

    image_data = asyncio.create_task(image.read())

    get_user_task =  asyncio.create_task(fetchone_document(Users, id=get_object_id(user_id)))

    if not verify_image(await image_data):
        raise BadRequestException("Invalid image or image type")

    user = await get_user_task

    if not user:
        raise NotFoundException("User does not exist")


    image_data = io.BytesIO(await image_data)

    _image = face_recognition.load_image_file(image_data)

    face_locations = face_recognition.face_locations(_image)

    if not face_locations:
        raise BadRequestException("Cannot proccess, No face found in the image.")


    top, right, bottom, left = face_locations[0]

    cropped_image = face_recognition.load_image_file(image_data)

    cropped_image = cropped_image[top:bottom, left:right]

    cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)

    file_path_for_user = os.path.join(os.getcwd(), f"static/model_data/{user_id}")

    os.makedirs(file_path_for_user, exist_ok=True)

    save_image_file_to_user(cropped_image, file_path_for_user)           

    return CustomResponse("Added Image To User Successfuly")



@router.post("/train-data")
async def train(request:Request):

    loss, accuracy = await train_evaluate_update(3, "static/model_data")

    print(loss)

    print(accuracy)

    data = {"accuracy": accuracy, "loss": loss}

    return CustomResponse("Model Trained Successfuly", data=data)