import freenect
import random
import time
import cv2
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
ctx = freenect.init()
while True:
    array,_ = freenect.sync_get_video()
    image = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    faces = face_cascade.detectMultiScale(image, 1.3, 3)
    print(faces)
    print(image.shape)
    freenect.sync_stop()
    dev = freenect.open_device(ctx, freenect.num_devices(ctx) - 1)
    print("dev opened")
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        print(f"Y: {y}, \n Image middle: {image.shape[1::-1][1] / 2}")
        image_height = image.shape[1::-1][1]
        image_middle = image_height / 2
        distance = image_middle - y
        print(distance)
        #freenect.set_tilt_degs(dev, tilt)
    cv2.imshow("im",image)
    freenect.close_device(dev)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit()