import os
import cv2
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




model = get_model(os.path.join(os.getcwd(), "model.pkl"))

known_faces = [face_obj.encoding for face_obj in model]

known_names = [f"{face_obj.firstname} {face_obj.lastname}" for face_obj in model]

known_ids = [str(face_obj.id) for face_obj in model]
    
known_is_blacklisted = [face_obj.is_blacklisted for face_obj in model]


def detect_faces(all_users:List[FaceEncoding]):

    global model

    global known_faces

    global known_names

    global known_is_blacklisted

    FRAME_THICKNESS = 5

    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()

        if not success:
            break

        locations = face_recognition.face_locations(frame)
    
        encodings = face_recognition.face_encodings(frame, locations)

        for face_encoding, face_location in zip(encodings, locations):
        
            results = face_recognition.compare_faces(known_faces, face_encoding, 0.5)

            if True in results:
                user_id_detect = known_ids[results.index(True)]

                targeted_user:Users = next((user for user in all_users if str(user.id) == user_id_detect), None)

                match = f"{targeted_user.firstname} {targeted_user.lastname}"


                is_known = IS_KNOWN if not targeted_user.is_blacklisted else IS_BLACKLISTED

            else:
                match = "Unknown"
                is_known = IS_UNKNOWN

            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])

            if is_known == IS_KNOWN:
                color = [0, 255, 0]

            elif is_known == IS_UNKNOWN:
                color = [0, 255, 255]

            else:
                color = [255, 0, 0]

            cv2.rectangle(frame, top_left, bottom_right, color, FRAME_THICKNESS)

            adjust_text_size(frame, match, face_location, is_known)



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