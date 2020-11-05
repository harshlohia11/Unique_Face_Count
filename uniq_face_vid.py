import cv2
import face_recognition
import argparse
from imutils import paths
import os

command2png = "ffmpeg -i myvid.mp4 -vf fps=1 images//image%d.png"
os.system(command2png)
# ARGPARSE FOR COMMOND-LINE INTERFACES ( * give folder name throug commond line )
ap = argparse.ArgumentParser()
ap.add_argument("-i","--images" ,required=True , help="path to input directory of images")

args = vars(ap.parse_args())
k=0
facelist=[]
face_encoding_list=[]
faces_recognized = 0
for imagePath in paths.list_images(args["images"]):
    image = cv2.imread(imagePath)
    
    rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_location_array = face_recognition.face_locations(rgb_frame)

    if face_location_array:
        top, right, bottom, left = face_location_array[0]
        faces_recognized += 1
        # print("[%i] Face recognized..." % faces_recognized)
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
        cropped_face = image[top:bottom, left:right]
        cv2.imwrite("faceimage.jpg", cropped_face)
        known_face = face_recognition.load_image_file("faceimage.jpg")
        try:
            # print(imagePath)
            biden_encoding = face_recognition.face_encodings(known_face)[0]
            # print(biden_encoding)
            face_encoding_list.append(biden_encoding)
        except:
            pass

l=(len(face_encoding_list))
# print(face_encoding_list)
# print(l)
for i in range(0,len(face_encoding_list)):
    k=0
    for j in range(i+1,len(face_encoding_list)):
        match = face_recognition.compare_faces([face_encoding_list[i]], face_encoding_list[j])
        if match[0]==True:
            k=k+1
    if k>0:
        l=l-1
print("NUMBER OF DISTINCT FACES = ",l)
