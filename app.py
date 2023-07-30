import os
import certifi
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from mongoengine import connect
from routers.user import router as user
from routers.video import router as video
from exceptions.custom_execption import *
from dotenv import load_dotenv

load_dotenv()



CERTIFICATE = os.path.join(os.path.dirname(certifi.__file__), "cacert.pem")




connect(host=os.getenv("MONGODB_URL"))


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user)
app.include_router(video)
app.add_exception_handler(UserExistExecption, user_exist_exception_handler)
app.add_exception_handler(UnauthorizedExecption, unauthorized_exception_handler)
app.add_exception_handler(ServerErrorException, server_exception_handler)
app.add_exception_handler(NotFoundException, not_found)
app.add_exception_handler(CredentialsException, credentail_exception_handler)
app.add_exception_handler(BadRequestException, bad_request_exception_handler)










