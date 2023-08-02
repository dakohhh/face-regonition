import pickle
import os
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
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




def get_train_test_data(path:str):

    

    for entry in os.scandir(path):

        if entry.is_dir():

            class_id = entry.path.split("\\")[-1]

            print(class_id)


    # for filename in os.listdir(os.path.join(os.getcwd(), "64c5783c513fe900cd712d52")):
    
    #     image = face_recognition.load_image_file(os.path.join(os.getcwd(), "64c5783c513fe900cd712d52", filename))

    #     face_locations = face_recognition.face_locations(image)

    #     img_cv2 = cv2.imread(os.path.join(os.getcwd(), f"64c5783c513fe900cd712d52/{filename}"))

    #     top, right, bottom, left = face_locations[0]

    #     cropped_face = img_cv2[top:bottom, left:right]

    #     grayscale_image = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2GRAY)

    #     scaled_cropped_grayscale_image = cv2.resize(grayscale_image, (40, 40))

    #     x.append(scaled_cropped_grayscale_image)
            
    #     y.append(1)






async def train_evaluate_update(lenght_of_user:int):


    # model = tf.keras.models.Sequential([

    #     tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(40, 40, 1)),
    #     tf.keras.layers.MaxPooling2D((2, 2)),
        
    #     tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    #     tf.keras.layers.MaxPooling2D((2, 2)),
        
    #     tf.keras.layers.Flatten(),
    #     tf.keras.layers.Dense(64, activation='relu'),
    #     tf.keras.layers.Dense(2, activation='softmax')
    # ])



    # model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    # model.fit(x_train, y_train, epochs=30)

    # test_loss, test_acc = model.evaluate(x_test, y_test)

    # test_loss, test_acc

    return 






# async def update_model(image_path:str, user:Users, model_path:str):
#     try:

#         with open(model_path, 'rb') as file:

#             encoding_model:List = pickle.load(file)

#             _ = await get_face_encodings_and_name(image_path, user)

#         encoding_model.append(_)

#         with open(model_path, 'wb') as file:

#             pickle.dump(encoding_model, file)

#     except:

#         encoding_model = []

#         _ = await get_face_encodings_and_name(image_path, user)

#         encoding_model.append(_)

#         with open(model_path, 'wb') as file:

#             pickle.dump(encoding_model, file)



def get_model(model_path:str) -> keras.Sequential:

    loaded_model = keras.models.load_model(model_path)

    return loaded_model



    





