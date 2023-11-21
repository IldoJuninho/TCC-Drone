import cv2
import math
import numpy as np
#import requests
import datetime
URL = "http://192.168.3.100:81/stream"
#webCamera = cv2.VideoCapture(0)
webCamera = cv2.VideoCapture(URL)
#classificadorAlvo = cv2.CascadeClassifier('Haarcascade/A1.xml')
#classificadorAlvo = cv2.CascadeClassifier('Haarcascade/cascade_alvo_central.xml')
#classificadorAlvo = cv2.CascadeClassifier('Haarcascade/12x12-pos24x24-neg32x24-1500n.xml')
classificadorAlvo = cv2.CascadeClassifier('Haarcascade/bolinhablk.xml')
classificadorVideoFace = cv2.CascadeClassifier('Haarcascade/haarcascade_frontalface_default.xml')
classificadorOlho = cv2.CascadeClassifier("Haarcascade/haarcascade_eye.xml")

vermelho = (0, 0, 255)
verde = (0, 255, 0)
azul = (255, 0, 0)

# webcam 640x480
# esp 320X240
width=320
height=240
width=width/2
height=height/2

lower_blue = np.array([100, 50, 50]) 
upper_blue = np.array([200, 200,200]) 
lower_blue1 = np.array([40, 20, 100]) 
upper_blue1 = np.array([100, 100,200]) 



frame_width = int(webCamera.get(3)) 
frame_height = int(webCamera.get(4)) 
   
size = (frame_width, frame_height)

result = cv2.VideoWriter("Videos\\"+datetime.datetime.now().strftime("%Y-%m-%d   %H;%M;%S")+'.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         10, size) 

result1 = cv2.VideoWriter("Videos\\"+datetime.datetime.now().strftime("%Y-%m-%d   %H;%M;%S")+'modf.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         10, size) 
   

while True:
	if webCamera.isOpened():  
	    camera, frame = webCamera.read()
	    #cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	    #detecta = classificadorAlvo.detectMultiScale(cinza)#cinza
	    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#cv2.COLOR_BGR2GRAY)
	    cinza = cv2.medianBlur(cinza,5)
	    rows = cinza.shape[0]
	    cinza = cv2.inRange(cinza, lower_blue,upper_blue)
	    cv2.imshow("smk", cinza)

	    detecta = classificadorAlvo.detectMultiScale(cinza)#cinza
	    #print(frame.shape[1])
	    #print(camera.shape[0])
	    for(x, y, l, a) in detecta:
	        #cv2.rectangle(frame, (x, y), (x + l, y + a), verde, 2)
	        cv2.circle(frame, (x+l//2, y+a//2), int((a//2)), verde, 2)
	        #cv2.line(frame, (int(width), int(height)), (x+l//2, int(height)), vermelho, 2)
	        #cv2.line(frame, (int(width), int(height)), (int(width), y+a//2), verde, 2)
	        #print(x,y,l,a)
	        #cv2.line(frame, (x, 240), (320, 240), vermelho, 1)
	        #cv2.line(frame, (320, y), (320, 240), verde, 1)
	        #cv2.line(frame, (180, 120), (x+l//2, 120), verde, 1)
	        #cv2.line(frame, (0, 0), (320, 240), verde, 1)
	        #print(x, l)
	        #print(frame.shape[1])
	        #print(frame.shape[0])

	        #pegaOlho = frame[y:y + a, x:x + l]
	        #OlhoCinza = cv2.cvtColor(pegaOlho, cv2.COLOR_BGR2GRAY)
	        #localizaOlho = classificadorOlho.detectMultiScale(OlhoCinza)
	        #for (ox, oy, ol, oa) in localizaOlho:
	            #cv2.rectangle(pegaOlho, (ox, oy), (ox + ol, oy + oa), (0, 255, 0), 2)

	    cv2.imshow("Video WebCamera", frame)
	    result1.write(frame) 
	
	    if cv2.waitKey(1) == ord('q'):
	        break
	else: 
		print("Algo deu errado")

webCamera.release()
cv2.destroyAllWindows()
