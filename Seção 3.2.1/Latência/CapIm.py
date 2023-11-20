import cv2
#import requests
URL = "http://192.168.3.100:81/stream"
#webCamera = cv2.VideoCapture(0)
webCamera = cv2.VideoCapture(URL)
classificadorAlvo = cv2.CascadeClassifier('Haarcascade/cascade_alvo_central.xml')
classificadorVideoFace = cv2.CascadeClassifier('Haarcascade/haarcascade_frontalface_default.xml')
classificadorOlho = cv2.CascadeClassifier("Haarcascade/haarcascade_eye.xml")

import datetime
dt = datetime.datetime.now()
dtn = datetime.datetime.now()
dt2 = datetime.datetime.now()
dtn2 = datetime.datetime.now()
dtq = datetime.datetime.now()
dtr = datetime.datetime.now()
print(dt)
dt.microsecond / 1000


vermelho = (0, 0, 255)
verde = (0, 255, 0)

# webcam 640x480
# esp 320X240
width=320
height=240
width=width/2
height=height/2

while True:
	if webCamera.isOpened(): 
	    dtn1 = datetime.datetime.now()
	    camera, frame = webCamera.read()
	    cv2.imshow("Video WebCamera", frame)
	    dtn2 = datetime.datetime.now()

	    dtm=dtn1-dt
	    dtm1=dtn2-dtn1
	    print("Loop",(dtm.microseconds/1000)," // Delay",(dtq))
	    dt=dtn1
	    dtq=float(dtm1.microseconds/1000)
	    
	
	    if cv2.waitKey(1) == ord('q'):
	        break
	else: 
		print("Algo deu errado")

webCamera.release()
cv2.destroyAllWindows()
