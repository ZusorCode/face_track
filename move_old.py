import freenect
import random
import time
import os
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
ctx = freenect.init()
font = cv2.FONT_HERSHEY_SIMPLEX
timeout = 0
save_im_cooldown = 0
last_x = 0
last_y = 0
last_w = 0
last_h = 0
cv2.namedWindow("im", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("im",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

while True:
    array,_ = freenect.sync_get_video()
    image = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    faces = face_cascade.detectMultiScale(image, 1.3, 4)
    
    if len(faces) != 0:
        freenect.sync_stop()
        dev = freenect.open_device(ctx, freenect.num_devices(ctx) - 1)
    
    if len(faces) != 0:
        for (x,y,w,h) in faces:
            last_x = x
            last_y = y
            last_w = w
            last_h = h
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
            image_height = image.shape[1::-1][1]
            steps = image_height / 30
            tilt =  30 - round(y / steps)
            print(tilt)
            freenect.set_tilt_degs(dev, tilt)
            if timeout < 20:
                timeout += 5
        freenect.close_device(dev)
    
    if len(faces) != 0 or timeout != 0:
        crop_img = image[last_y:last_y+last_h, last_x:last_x+last_w]
        r = 100.0 / crop_img.shape[1]
        dim = (100, int(crop_img.shape[0] * r))
        crop_img = cv2.resize(crop_img, dim, interpolation = cv2.INTER_AREA)
        image[50:50+crop_img.shape[0], 50:50+crop_img.shape[1]] = crop_img

    if len(faces) != 0 and save_im_cooldown == 0:
            imname = str(time.time()).replace(".", "") + ".png"
            cv2.imwrite(imname, image)
            os.rename(imname, f"Faces/" + imname)
            save_im_cooldown = 30
    if timeout > 0:
        timeout -= 1
    if save_im_cooldown > 0:
        save_im_cooldown -= 1
    cv2.imshow("im",image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit()