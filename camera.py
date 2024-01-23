import cv2,time
def streaming(camera_id):
    link="Data\\"+str(camera_id)+".avi" 
    cap = cv2.VideoCapture(link)
    # Read stream
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, img = cap.read()
        if ret == True:
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 

            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(1/30)
        else: 
            break

def thumbnail(camera_id):
    link="Data\\"+str(camera_id)+".avi"
    cap = cv2.VideoCapture(link)
    # Read stream
        # Capture frame-by-frame
    ret, img = cap.read()
    if ret == True:
        img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def Parking(area_id):
    link="Data\\"+"Parking\\"+str(area_id)+".mp4" 
    cap = cv2.VideoCapture(link)
    # Read stream
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, img = cap.read()
        if ret == True:
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 

            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(1/30)
        else: 
            break

def parkingthumbnail(area_id):
    link="Data\\"+"Parking\\"+str(area_id)+".mp4" 
    cap = cv2.VideoCapture(link)
    # Read stream
        # Capture frame-by-frame
    ret, img = cap.read()
    if ret == True:
        img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


