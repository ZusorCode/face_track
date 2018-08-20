import freenect
import cv2
import frame_convert2
import random
import time

cv2.namedWindow("RGB", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("RGB",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
keep_running = True
last_time = 0
faceFound = False
last_x = 0
last_y = 0
last_w = 0
last_h = 0
tilt = 15
timeout = 0

def display_depth(dev, data, timestamp):
    global keep_running

def display_rgb(dev, data, timestamp):
    global keep_running, tilt, faceFound, timeout
    image = cv2.cvtColor(data, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
    
    if len(faces) != 0:
        faceFound = True
        if timeout < 20:
            timeout += 1
        for (x,y,w,h) in faces:
            last_x = x
            last_y = y
            last_w = w
            last_h = h
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
            image_height = image.shape[1::-1][1]
            steps = image_height / 30
            tilt = 30 - round(y / steps)
    if len(faces) == 0:
        faceFound = False
        if timeout > 14:
            timeout -= 1
            tilt = 15
        if timeout >= 15:
            cv2.rectangle(image,(last_x,last_y),(last_x+last_w,last_y+last_h),(255,0,0),2)
            image_height = image.shape[1::-1][1]
            steps = image_height / 30
            tilt = 30 - round(y / steps)

    cv2.imshow('RGB', image)
    if cv2.waitKey(10) == 27:
        keep_running = False


def body(dev, ctx):
    global last_time, tilt0
    if not keep_running:
        raise freenect.Kill
    if time.time() - last_time < 1:
        return
    
    last_time = time.time()
    led = 2
    if faceFound and abs(tilt - tilt0) > 0:
        led = 3
    if faceFound and abs(tilt - tilt0) == 0:
        led = 4
    tilt0 = tilt
    freenect.set_led(dev, led)
    freenect.set_tilt_degs(dev, tilt)
    print('led[%d] tilt[%d] accel[%s]' % (led, tilt, freenect.get_accel(dev)))
    if not keep_running:
        raise freenect.Kill

freenect.runloop(depth=display_depth, video=display_rgb, body=body)
