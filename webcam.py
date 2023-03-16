import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
frame_index = 0

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    frame_index += 1
    print(frame_index)
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if frame_index % 10 == 0:
        cv2.imwrite(f"images/scr{frame_index}.jpg", frame)
    if frame_index == 100:
        break
    # if key == 27: # exit on ESC
    # #     cv2.imwrite(f"scr{frame_index}.jpg", frame)
    #     break

vc.release()
cv2.destroyWindow("preview")