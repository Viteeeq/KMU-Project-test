import cv2
import face_recognition
import sqlite3
from itertools import count
import json
import os
import numpy as np
from PIL import Image
import time

# Функция, которая добавляет эталонную фотографию(с ней будет сравниваться видео загруженное в ТГ)
def extracting_faces(img_path, username):
    faces = face_recognition.load_image_file(img_path)
    faces_locations = face_recognition.face_locations(faces)

    for face_location in faces_locations:
        top, right, bottom, left = face_location

        face_img = faces[top:bottom, left:right]
        pil_img = Image.fromarray(face_img)
        pil_img.save(f"{username}.jpg")
    known_photo = face_recognition.load_image_file(f"{username}.jpg")
    known_encodings = np.array(face_recognition.face_encodings(known_photo)[0]).tolist()
    print(known_encodings)
    return json.dumps(known_encodings)

def frame_count(temp):
    video = f"{temp}.mp4"
    video_capture = cv2.VideoCapture(video)
    frame_array = []
    cur_vr = 0
    max_vr = 0
    frame_array_cur = [[0, 0]]
    length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    print(length)
    while True:
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        first_face_location = face_recognition.face_locations(rgb_small_frame)
        if len(first_face_location) == 0:
            frame_array.append(0)
            if len(frame_array) == length:
                break
            continue
        else:
            frame_array.append(1)
            if len(frame_array) == length:
                break
            else:
                continue
    frame_array.insert(0, 0)
    frame_array.insert(len(frame_array), 0)
    for x in range(1,len(frame_array)):
        if (frame_array[x-1] == 0 and frame_array[x] == 1):
            frame_array_cur.append([x, x])
        if (frame_array[x-1] == 1 and frame_array[x] == 0):
            frame_array_cur[len(frame_array_cur)-1][1] = x-1
    if len(frame_array_cur) != 1:
        for x in range(len(frame_array_cur)):
            cur_vr = frame_array_cur[x][1] - frame_array_cur[x][0]
            if max_vr < cur_vr:
                max_vr = cur_vr
                res = frame_array_cur[x]
        res[0] = res[0] - 1
        res[1] = res[1] - 1
    else:
        res = [0, 0]
    fin = res[1] - res[0] + 1
    return res, fin

# Функция, которая вырезает из видео 3 идеальных кадра
def save_src(temp, res, fin):
    video = f"{temp}.mp4"
    video_capture = cv2.VideoCapture(video)
    have_face = False
    den = int(round(fin/3))
    length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    final = [even_frame * den for even_frame in range(3)]
    fr_num = [even_frame + res[0] for even_frame in final]
    if fin > 1:
        have_face = True
        while True:
            frame_id = int(round(video_capture.get(1)))
            _, frame = video_capture.read()
            if frame_id == fr_num[1]:
                cv2.imwrite(f"scr{frame_id}.jpg", frame)
            if frame_id == length - 1:
                break
        print(fr_num[1])
    else:
        have_face = False
    
    return have_face, fr_num[1]

def discr_compare(known_enc, destination):
    image_to_compare = face_recognition.load_image_file(destination)  # загружаем фото которое надо сравнить
    image_to_compare_encoding = face_recognition.face_encodings(image_to_compare)[0]  # вычисляем дескриптор
    result = face_recognition.compare_faces([known_enc], image_to_compare_encoding, tolerance=0.5)  # получаем результат сравнения
    return result

def cleaning(frame):
    os.remove(f'scr{frame}.jpg')

# start_time = time.time()
# a, b = frame_count("temp_video")
# save_src("temp_video", a, b)
# print("--- %s seconds ---" % (time.time() - start_time))

print(discr_compare([0.004332992248237133, 0.1089041605591774, 0.04482821375131607,
                     -0.052875351160764694, -0.017979919910430908, -0.01927122287452221,
                     -0.012411988340318203, -0.07055283337831497, 0.20332059264183044, -0.11977101862430573, 0.17699678242206573, 0.027642611414194107, -0.28285035490989685, -0.09736377745866776, -0.047910552471876144, 0.05815833806991577, -0.05274784564971924, -0.12451587617397308, -0.06225598603487015, -0.0456346794962883, 0.07727747410535812, 0.05081315338611603, -1.3315875548869371e-05, 0.017644425854086876, -0.11727438867092133, -0.267092227935791, -0.05706459656357765, -0.1590857356786728, -0.04791351780295372, -0.07618316262960434, -0.0750543475151062, 0.1588360220193863, -0.06161527708172798, -0.07139012217521667, 0.05419149994850159, 0.07934492081403732, -0.008887446485459805, 0.05631517991423607, 0.20329894125461578, 0.07539123296737671, -0.15720100700855255, -0.019006891176104546, -0.004080003127455711, 0.3105342984199524, 0.21477441489696503, -0.023363519459962845, 0.029087655246257782, -0.05812004208564758, 0.17066653072834015, -0.27144235372543335, 0.09309911727905273, 0.15087518095970154, 0.16864125430583954, 0.09690113365650177, 0.16286709904670715, -0.15671411156654358, 0.020510438829660416, 0.09385688602924347, -0.23065651953220367, 0.12655392289161682, 0.06386271864175797, -0.15898969769477844, -0.0795091912150383, -0.014457411132752895, 0.19778956472873688, 0.08833667635917664, -0.12968654930591583, -0.10238276422023773, 0.2084895819425583, -0.17538602650165558, -0.05218759924173355, 0.12551428377628326, -0.13992606103420258, -0.14296285808086395, -0.1926453560590744, 0.056890882551670074, 0.3653833568096161, 0.22663924098014832, -0.1769595742225647, 0.048906393349170685, -0.10082487016916275, -0.02352631650865078, 0.07086776196956635, 0.057260408997535706, -0.05192763730883598, 0.048630982637405396, -0.03638329356908798, 0.0003326237201690674, 0.14267109334468842, 0.009850049391388893, -0.07502278685569763, 0.2633739411830902, -0.01826997846364975, 0.07884868234395981, 0.07919654250144958, -0.041623033583164215, -0.0444490984082222, -0.07635711878538132, -0.17818288505077362, -0.038433849811553955, -0.018864165991544724, -0.1864432692527771, -0.0029915212653577328, 0.06062779575586319, -0.16340932250022888, 0.09358549118041992, -0.04823779687285423, 0.03748851269483566, -0.024708759039640427, -0.016284309327602386, -0.09188499301671982, 0.0047287652269005775, 0.18070250749588013, -0.2740558087825775, 0.18038882315158844, 0.09349670261144638, 0.07576431334018707, 0.09231018275022507, 0.04484464228153229, 0.008656862191855907, 0.04312271252274513, -0.13944511115550995, -0.13161028921604156, -0.07956648617982864, 0.07788600772619247, -0.005681228823959827, 0.04231740161776543, -0.010331384837627411], "randomname.jpg"))