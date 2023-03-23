import face_recognition
import time

start_time = time.time()
image_to_compare = face_recognition.load_image_file("snapshot.jpg")  # загружаем фото которое надо сравнить
image_to_compare_encoding = face_recognition.face_encodings(image_to_compare)[0]  # вычисляем дескриптор
# print(image_to_compare_encoding)
x = time.time() - start_time
print(round(x, 3))
image_to_compare = face_recognition.load_image_file("randomname.jpg")  # загружаем фото которое надо сравнить
image_to_compare_encoding = face_recognition.face_encodings(image_to_compare)[0]  # вычисляем дескриптор
y = time.time() - start_time - x
print(round(y,3))
print(f'Разница равна {x - y}')