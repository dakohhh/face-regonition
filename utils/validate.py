from bson import ObjectId
from PIL import Image
from exceptions.custom_execption import BadRequestException




def get_object_id(id:str):
    try:
        return ObjectId(id)
    
    except:
        raise BadRequestException("Invalid Id")
    


async def verify_image(image_bytes:bytes):
    try:
        im  = Image.frombytes('RGBA', (128,128), image_bytes, 'raw')

        im.verify()
        return True
    except:
        return False