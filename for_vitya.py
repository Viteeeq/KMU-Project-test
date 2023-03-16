import cv2

cap = cv2.VideoCapture(0)  # инициализируем захват видео
frame_count = 0  # счетчик кадров

while True:
    ret, frame = cap.read()  # считываем следующий кадр

    if not ret:  # если чтение кадра не удалось, выходим из цикла
        break

    frame_count += 1  # увеличиваем счетчик кадров на 1

    if frame_count % 10 == 0:  # если кадр является кратным 10, обрабатываем его
        # здесь можно добавить свой код обработки кадра
        cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # если нажата клавиша 'q', выходим из цикла
        break

cap.release()  # освобождаем ресурсы
cv2.destroyAllWindows()  # закрываем все окна