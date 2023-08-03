import os
import cv2
import numpy as np
import asyncio
import face_recognition
from typing import List
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from database.schema import Users
from utils.model_func import get_model, FaceEncoding, IS_KNOWN, IS_BLACKLISTED, IS_UNKNOWN
from utils.video_func import adjust_text_size


router = APIRouter(tags=["Video"], prefix="/video")

templates = Jinja2Templates(directory="templates")


model = asyncio.create_task(get_model(os.path.join(os.getcwd(), "tf_face_model.h5")))

class_list = ["Wisdom", "Joshua"]

async def detect_faces(all_users):

    global model

    global class_list

    FRAME_THICKNESS = 5

    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()

        if not success:
            break

        locations = face_recognition.face_locations(frame)
    
        for face_location in locations:

            top, right, bottom, left = face_location

            cropped_face = frame[top:bottom, left:right]


            grayscale_image = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2GRAY)


            scaled_cropped_grayscale_image = cv2.resize(grayscale_image, (40, 40))

            prediction = model.predict(np.array([scaled_cropped_grayscale_image]))

            match = class_list[np.argmax(prediction)]

            color = [0, 255, 0]

            cv2.rectangle(frame, (left, top), (right, bottom), color, FRAME_THICKNESS)

            adjust_text_size(frame, match, face_location, IS_KNOWN)



        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()





@router.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("video.html", {"request": request})





@router.get('/feed')
def video_feed():
    all_users = Users.objects.all()

    return StreamingResponse(detect_faces(all_users), media_type='multipart/x-mixed-replace; boundary=frame')