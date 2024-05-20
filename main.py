import cv2
import time
from datetime import datetime
import glob
import os
from threading import Thread

from send_email import send_email


video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1


def clean_folder():
    images = glob.glob('images/*.png')
    for image in images:
        os.remove(image)


while True:

    status = 0
    check, frame = video.read()

    # Add timestamp
    now = datetime.now()

    cv2.putText(img=frame, text=now.strftime('%Y / %m / %d'), org=(30, 20),
                fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1,
                color=(255, 0, 0), thickness=1, lineType=cv2.LINE_AA)

    cv2.putText(img=frame, text=now.strftime('%H:%M:%S'), org=(30, 40),
                fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1,
                color=(255, 0, 0), thickness=1, lineType=cv2.LINE_AA)

    email_timestamp = now.strftime('%Y/%m/%d at %H:%M:%S')

    # Movement Detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gauss_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gauss_frame

    delta_frame = cv2.absdiff(first_frame, gauss_frame)
    threshold_frame = cv2.threshold(delta_frame, 70, 255, cv2.THRESH_BINARY)[1]
    dilated_frame = cv2.dilate(threshold_frame, None, iterations=2)
    contours, check = cv2.findContours(dilated_frame, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            captured_images = glob.glob("images/*.png")
            index = int(len(captured_images) / 2)
            culprit = captured_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email,
                              args=(culprit, email_timestamp))
        email_thread.daemon = True
        email_thread.start()

    cv2.imshow("Movement detection", frame)

    key = cv2.waitKey(1)

    if key == ord("c"):
        clean_folder()
        break

video.release()

