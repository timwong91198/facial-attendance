# * --------- IMPORTS ---------*
import cv2
import face_recognition
import imutils
from imutils.video import VideoStream
import numpy as np
import time
import argparse
import os
import re
import pickle

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

# load the known faces and embeddings
print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())

# Select the webcam of the computer (0 by default for laptop)
video_capture = VideoStream(src=1).start()

# Aplly it until you stop the file's execution
while True:
    # Take every frame

    # process_this_frame = True
    # Process every frame only one time
    # if process_this_frame:
    # Find all the faces and face encodings in the current frame of video
    frame = video_capture.read()

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb = imutils.resize(frame, width=750)
    r = frame.shape[1] / float(rgb.shape[1])

    face_locations = face_recognition.face_locations(rgb, model=args["detection_method"])
    face_encodings = face_recognition.face_encodings(rgb, face_locations)
    # Initialize an array for the name of the detected users
    face_names = []

    # * ---------- Initialyse JSON to EXPORT --------- *
    #    json_to_export = {}
    # loop over the facial embeddings
    for encoding in face_encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
                                                 encoding)
        name = []

        face_distances = face_recognition.face_distance(data["encodings"], encoding)

        best_match_index = np.argmin(face_distances)

        print(face_distances)
        # check to see if we have found a match

        # find the indexes of all matched faces then initialize a
        # dictionary to count the total number of times each face
        # was matched
        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                if face_distances.all() < 0.46:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                else:
                    name = "Unknown"
            else:
                pass
        else:
            pass

            # name = max(counts, key=counts.get)

            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)

            # matchedIdxs = [i for (i, b) in enumerate(matches) if b]

            # for i in matchedIdxs:

            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched

            # loop over the matched indexes and maintain a count for
            # each recognized face face

            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)

        # update the list of names
        #  face_names.append(name)
        # * ---------- SAVE data to send to the API -------- *
        # Save the name
        # json_to_export['name'] = name
        # Save the time
        # json_to_export['hour'] = f'{time.localtime().tm_hour}:{time.localtime().tm_min}'
        # Save the date
        # json_to_export[
        #   'date'] = f'{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday}'
        # If you need to save a screenshot:
        # json_to_export['picture_array'] = frame.tolist()

        # * ---------- SEND data to API --------- *
        # Make a POST request to the API
        # r = requests.post(url='http://127.0.0.1:5000/receive_data', json=json_to_export)
        # Print to status of the request:
        # print("Status: ", r.status_code)

        # Store the name in an array to display it later
        # face_names.append(name)
        # To be sure that we process every frame only one time
        # process_this_frame = not process_this_frame

        # Store the name in an array to display it later
        face_names.append(name)
        print(name)
        # To be sure that we process every frame only one time
    # process_this_frame = not process_this_frame

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(face_locations, face_names):
        # rescale the face coordinates
        top = int(top * r)
        right = int(right * r)
        bottom = int(bottom * r)
        left = int(left * r)

        # draw the predicted face name on the image
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        # cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
        #             1, (0, 255, 0), 2, lineType=cv2.LINE_AA)

        # Display the resulting image
    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
