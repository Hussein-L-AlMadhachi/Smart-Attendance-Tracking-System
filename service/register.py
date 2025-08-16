import face_recognition
import os
import pickle



# globals
known_faces_dir = "known_faces"
known_encodings = []
known_names = []



def register_faces():        

    for file_name in os.listdir(known_faces_dir):
        if file_name.lower().endswith(('jpg', 'jpeg', 'png')):
            image_path = os.path.join(known_faces_dir, file_name)
            image = face_recognition.load_image_file(image_path)
            
            # Generate face encoding (assumes one face per image)
            encoding = face_recognition.face_encodings(image)
            if len(encoding) > 0:
                known_encodings.append(encoding[0])
                name = os.path.splitext(file_name)[0]  # Use filename as name
                known_names.append(name)
            else:
                print(f"No face detected in {file_name}")

    # Save encodings to disk for reuse
    with open("face_encodings.pkl", "wb") as f:
        print( known_encodings )
        print( known_names )
        pickle.dump((known_encodings, known_names), f)

    print("Face encodings saved!")


