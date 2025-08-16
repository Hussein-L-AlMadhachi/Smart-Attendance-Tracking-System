import cv2
import face_recognition
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
import os






def monitor_faces():
    # Load known face encodings
    with open("face_encodings.pkl", "rb") as f:
        known_encodings, known_names = pickle.load(f)

    # Initialize attendance log
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    attendance_file = f"attendance/attendance-{today}.csv"
    df = pd.DataFrame(columns=["Name", "Timestamp"])
    df.to_csv(attendance_file, index=False)

    # Start webcam
    video_capture = cv2.VideoCapture(0)

    # Keep track of who's already marked today
    marked_today = set()

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Find all face locations and encodings in current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare with known faces
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"

            # Use the known face with the smallest distance
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]

            # Mark attendance if recognized and not already marked today
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if name != "Unknown" and name not in marked_today:
                with open(attendance_file, 'a') as f:
                    f.write(f"\n\"{name}\",\"{now}\"\n")
                marked_today.add(name)
                print(f"Attendance marked: {name} at {now}")

            # Draw box and label on face
            top, right, bottom, left = face_location
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # Display the video
        cv2.imshow("Attendance System - Press 'q' to quit", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()





def monitor_faces_headless():
    # Load known face encodings
    with open("face_encodings.pkl", "rb") as f:
        known_encodings, known_names = pickle.load(f)

    # Initialize attendance log
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    attendance_file = f"attendance/attendance-{today}.csv"
    df = pd.DataFrame(columns=["Name", "Timestamp"])
    df.to_csv(attendance_file, index=False)

    # Start webcam
    video_capture = cv2.VideoCapture(0)

    # Keep track of who's already marked today
    marked_today = set()

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Find all face locations and encodings in current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare with known faces
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"

            # Use the known face with the smallest distance
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]

            # Mark attendance if recognized and not already marked today
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if name != "Unknown" and name not in marked_today:
                with open(attendance_file, 'a') as f:
                    f.write(f"\n\"{name}\",\"{now}\"")
                marked_today.add(name)
                print(f"Attendance marked: {name} at {now}")

            # Draw box and label on face
            top, right, bottom, left = face_location
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            #cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            #cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # Display the video
        #cv2.imshow("Attendance System - Press 'q' to quit", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()




