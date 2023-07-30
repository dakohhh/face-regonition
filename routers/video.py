import os
import cv2
import face_recognition
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from utils.model_func import get_model
from utils.video_func import adjust_text_size


router = APIRouter(tags=["Video"], prefix="/video")

model = get_model(os.path.join(os.getcwd(), "model.pkl"))

known_faces = [face_obj.encoding for face_obj in model]

known_names = [f"{face_obj.firstname} {face_obj.lastname}" for face_obj in model]
    
known_is_blacklisted = [face_obj.is_blacklisted for face_obj in model]


def detect_faces():

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
    
        encodings = face_recognition.face_encodings(frame, locations, model="hog")

        for face_encoding, face_location in zip(encodings, locations):
        
            results = face_recognition.compare_faces(known_faces, face_encoding, 0.5)

            if True in results:
                match = "Wisdom"
                print(known_names[results.index(True)])

                is_known = True

            else:
                match = "Unknown"
                is_known = False


            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])
            color = [0, 255, 0] if is_known else [0, 255, 255]


            cv2.rectangle(frame, top_left, bottom_right, color, FRAME_THICKNESS)

            adjust_text_size(frame, match, face_location, is_known)



        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()



@router.get('/feed')
def video_feed():
    return StreamingResponse(detect_faces(), media_type='multipart/x-mixed-replace; boundary=frame')