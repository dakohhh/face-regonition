from bson import ObjectId
from exceptions.custom_execption import BadRequestException




def get_object_id(id:str):
    try:
        return ObjectId(id)
    
    except:
        raise BadRequestException("Invalid Id")