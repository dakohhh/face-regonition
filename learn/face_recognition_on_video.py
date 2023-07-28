import os
import cv2
import pickle
import face_recognition


KNOWN_FACES_DIR = "knowned"

UNKNOWN_FACES_DIR = "unknowed"

FRAME_THICKNESS = 5

def get_face_encodings_and_name():
    
    known_faces = []

    known_names = []

    for name in os.listdir(os.path.join(os.getcwd(), KNOWN_FACES_DIR)):
        print("Name", name)

    for image_filename in os.listdir(os.path.join(os.getcwd(), f'{KNOWN_FACES_DIR}/{name}')):
        
        print("Image Filename", image_filename)
        
        image = face_recognition.load_image_file(os.path.join(os.getcwd(), f'{KNOWN_FACES_DIR}/{name}/{image_filename}'))
        
        encoding = face_recognition.face_encodings(image, model="hog")[0]
            
        known_faces.append(encoding)
        
        known_names.append(name)


    with open('model.pkl', 'wb') as file:

        pickle.dump((known_faces, known_names), file)

    return (known_faces, known_names)






def adjust_text_size(frame, match, face_location, is_known):
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (face_location[3] + 10, face_location[2] + 15)
    color = (200, 200, 200)
    thickness = 2

    if is_known:
        font_scale = 1.0
        thickness = 2
    else:
        font_scale = 0.5

    cv2.putText(frame, match, org, font, font_scale, color, thickness, cv2.LINE_AA)








try:
    with open('model.pkl', 'rb') as file:
        encoding_model = pickle.load(file)

except FileNotFoundError:

    encoding_model = get_face_encodings_and_name()





known_faces, known_names = encoding_model

camera = cv2.VideoCapture(0)


while True:
    success, frame = camera.read()

    if not success:
        break


    locations = face_recognition.face_locations(frame)
    
    encodings = face_recognition.face_encodings(frame, locations, model="hog")



    for face_encoding, face_location in zip(encodings, locations):
        
        results = face_recognition.compare_faces(known_faces, face_encoding, 0.5)

        print(results)

        if True in results:
            match = known_names[results.index(True)]

            is_known = True

        else:
            match = "Unknown"
            is_known = False




        top_left = (face_location[3], face_location[0])
        bottom_right = (face_location[1], face_location[2])
        color = [0, 255, 0] if is_known else [255, 255, 0]
        cv2.rectangle(frame, top_left, bottom_right, color, FRAME_THICKNESS)

        adjust_text_size(frame, match, face_location, is_known)

    cv2.imshow('Real-Time Face Detection', frame)


    if cv2.waitKey(1) & 0xFF == ord('b'):
        break



camera.release()

cv2.destroyAllWindows()






