#!/usr/bin/env python
import freenect
import cv2
import numpy as np

cv2.namedWindow('Video', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def video():
    array, _ = freenect.sync_get_video()
    return cv2.cvtColor(array, cv2.COLOR_RGB2BGR)

while 1:
    img = video()
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    
    if len(faces) != 0:
        for (x,y,w,h) in faces:
            last_x = x
            last_y = y
            last_w = w
            last_h = h
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
            image_height = image.shape[1::-1][1]
    
    if len(faces) != 0 or timeout != 0:
        crop_img = image[last_y:last_y+last_h, last_x:last_x+last_w]
        r = 100.0 / crop_img.shape[1]
        dim = (100, int(crop_img.shape[0] * r))
        crop_img = cv2.resize(crop_img, dim, interpolation = cv2.INTER_AREA)
        image[50:50+crop_img.shape[0], 50:50+crop_img.shape[1]] = crop_img

    
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        
    cv2.imshow('Video', img)
    if cv2.waitKey(10) == 27:
        break