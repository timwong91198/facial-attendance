import cv2
import face_recognition
import imutils
from imutils.video import VideoStream
from datetime import datetime
import numpy as np
import time
import argparse
import pickle
import threading
from multiprocessing import Process
import sys
import openpyxl

db = openpyxl.load_workbook('D:\\Google Drive\\Software Files\\PyCharm\\Facial Rec')
dateTime = datetime.now()

x = []

ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", default="D:\\Dropbox\\Dropoff\\encodings.pickle",
                help="path to serialized db of facial encodings")
ap.add_argument("-o", "--output", type=str,
                help="path to output video")
ap.add_argument("-y", "--display", type=int, default=1,
                help="whether or not to display output frame to screen")
ap.add_argument("-d", "--detection_method", type=str, default="hog",
                help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())

video_capture = VideoStream(src=0).start()

while True:

    frame = video_capture.read()

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb = imutils.resize(frame, width=750)
    r = frame.shape[1] / float(rgb.shape[1])

    face_locations = face_recognition.face_locations(rgb, model=args["detection_method"])
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    face_names = []

    for encoding in face_encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)

        face_distances = face_recognition.face_distance(data["encodings"], encoding)

        best_match_index = np.argmin(face_distances)

        print(face_distances)
        name_lists = ["xue wen", "Tim", "han qing", "yc"]
        name = []

        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matchedIdxs:
                if face_distances.all() < 0.46:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                    for item in name_lists:
                        if name == item:
                            print("login success")
                            print(dateTime)
                            print(name)
                            x.append(name)
                            print(x)
                    for things in x:
                        if name == things:
                            #  detect but send one time log out to database
                            print("logout success")
                            print(dateTime)
                            print(name)
                            x.remove(name)
                            print(x)
                else:
                    name = "Unknown"

    for ((top, right, bottom, left), name) in zip(face_locations, face_names):
        top = int(top * r)
        right = int(right * r)
        bottom = int(bottom * r)
        left = int(left * r)

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15

    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

video_capture.release()
cv2.destroyAllWindows()
