import face_recognition
import time
import deepface

# start_time = time.time()
# image_to_compare = face_recognition.load_image_file("snapshot.jpg")  # загружаем фото которое надо сравнить
# image_to_compare_encoding = face_recognition.face_encodings(image_to_compare)[0]  # вычисляем дескриптор
# # print(image_to_compare_encoding)
# x = time.time() - start_time
image_to_compare = face_recognition.load_image_file("randomname.jpg")  # загружаем фото которое надо сравнить
print(face_recognition.face_landmarks(image_to_compare))
image_to_compare_encoding = face_recognition.face_encodings(image_to_compare)[0]  # вычисляем дескриптор