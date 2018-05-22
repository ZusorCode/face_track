import freenect
import random
import time
import cv2
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
ctx = freenect.init()
cv2.namedWindow("im", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("im",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
while True:
    array,_ = freenect.sync_get_video()
    image = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    faces = face_cascade.detectMultiScale(image, 1.3, 4)
    if len(faces) != 0:
        freenect.sync_stop()
        dev = freenect.open_device(ctx, freenect.num_devices(ctx) - 1)
        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
            image_height = image.shape[1::-1][1]
            steps = image_height / 30
            tilt =  30 - round(y / steps)
            print(tilt)
            freenect.set_tilt_degs(dev, tilt)
        freenect.close_device(dev)
    cv2.imshow("im",image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit()