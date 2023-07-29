from typing import List, Union
from fastapi import Form
from pydantic import BaseModel, validator, Field
from bson import ObjectId
from exceptions.custom_execption import BadRequestException


class TokenData(BaseModel):
    username:str
    user_id: str
    refresh_token: Union[str, None]
    expire: int





class CreateUser(BaseModel):
    firstname:str
    lastname:str
    matric_no:int