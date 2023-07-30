import pickle
import face_recognition
from typing import List
from database.schema import Users
from exceptions.custom_execption import BadRequestException




IS_UNKNOWN = 0

IS_KNOWN = 1

IS_BLACKLISTED = 2


class FaceEncoding():

    def __init__(self, id, firstname, lastname, is_blacklisted, encoding):

        self.id=id
        self.firstname=firstname
        self.lastname=lastname
        self.encoding=encoding
        self.is_blacklisted= is_blacklisted



async def get_face_encodings_and_name(image_path:str, user:Users):

    image = face_recognition.load_image_file(image_path)
    
    encoding = face_recognition.face_encodings(image, model="hog")[0]
        
    return FaceEncoding(user.id, user.firstname, user.lastname, user.is_blacklisted, encoding)



async def update_model(image_path:str, user:Users, model_path:str):
    try:

        with open(model_path, 'rb') as file:

            encoding_model:List = pickle.load(file)

            _ = await get_face_encodings_and_name(image_path, user)

        encoding_model.append(_)

        with open(model_path, 'wb') as file:

            pickle.dump(encoding_model, file)

    except:

        encoding_model = []

        _ = await get_face_encodings_and_name(image_path, user)

        encoding_model.append(_)

        with open(model_path, 'wb') as file:

            pickle.dump(encoding_model, file)



def get_model(model_path:str) ->List[FaceEncoding]:

    try:
        with open(model_path, 'rb') as file:

            encoding_model:List = pickle.load(file)

        
        return encoding_model


    except FileNotFoundError:

        raise BadRequestException("Model not found, please train model")



    





