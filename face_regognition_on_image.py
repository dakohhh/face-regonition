import os
import numpy
import cv2
import matplotlib.pyplot as plt
import face_recognition



KNOWN_FACES_DIR = "knowned"

UNKNOWN_FACES_DIR = "unknowed"

TOLERANCE = 0.4

FRAME_THICKNESS = 10

FONT_THICKNESS = 2

MODEL ="hog"

images = []

known_faces = []

known_names = []

face_locations = []


for name in os.listdir(os.path.join(os.getcwd(), KNOWN_FACES_DIR)):
    print("Name", name)

    for image_filename in os.listdir(os.path.join(os.getcwd(), f'{KNOWN_FACES_DIR}/{name}')):
        
        print("Image Filename", image_filename)
        
        image = face_recognition.load_image_file(os.path.join(os.getcwd(), f'{KNOWN_FACES_DIR}/{name}/{image_filename}'))
        
        encoding = face_recognition.face_encodings(image, model=MODEL)[0]
        
        locations = face_recognition.face_locations(image)[0]
        
        face_locations.append(locations)
        
        images.append(image)
        
        known_faces.append(encoding)
        
        known_names.append(name)
        



found_faces = []

for unknown_image_filename in os.listdir(UNKNOWN_FACES_DIR):
    print(unknown_image_filename)
    
    image = face_recognition.load_image_file(os.path.join(UNKNOWN_FACES_DIR, unknown_image_filename))
    
    locations = face_recognition.face_locations(image)
    
    encodings = face_recognition.face_encodings(image, locations, model=MODEL)
    
    bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    for face_encoding, face_location in zip(encodings, locations):
        
        results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)

        match = None

        if True in results:

            match = known_names[results.index(True)]

            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])
            color = [0, 255, 0]
            cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)


            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2] + 22)
            color = [0, 255, 0]
            cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
            
            
            font = cv2.FONT_HERSHEY_SIMPLEX

            org = (face_location[3] + 10, face_location[2] + 15)
              
            fontScale = 5
               
            color = (200, 200, 200)
              
            thickness = 5
               
            cv2.putText(image, 
                        match, 
                        org, font, 
                        fontScale, 
                        color, thickness, cv2.LINE_AA)
            

    cv2.namedWindow(unknown_image_filename, cv2.WINDOW_NORMAL)

    cv2.resizeWindow(unknown_image_filename, 50, 50)

    cv2.imshow(unknown_image_filename, image)
    cv2.waitKey(0)
    cv2.destroyWindow(unknown_image_filename)
            
        
            


