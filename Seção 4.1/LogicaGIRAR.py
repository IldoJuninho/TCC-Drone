import pyfirmata
import time
import serial.tools.list_ports as portlist
import numpy as np
pinE=5
pinD=4
pinC=2
pinB=3
pinA=8
pinH=9

ports = list( portlist.comports() )
for p in ports:
  print(p)


port="/dev/ttyACM0"
board = pyfirmata.Arduino(port)

import cv2
#import requests
URL = "http://192.168.3.101:81/stream"
# webCamera = cv2.VideoCapture(0)
webCamera = cv2.VideoCapture(URL)

classificadorCirculoExterno = cv2.CascadeClassifier('Haarcascade/A1.xml')
classificadorCirculoInterno = cv2.CascadeClassifier('Haarcascade/cascade_alvo_central.xml')
classificadorCirculoIntermediario = cv2.CascadeClassifier('Haarcascade/12x12-pos24x24-neg32x24-1500n.xml')
classificadorBolinhaAzul = cv2.CascadeClassifier('Haarcascade/bolinhablk.xml')
classificadorAF = cv2.CascadeClassifier('Haarcascade/AlvoF.xml')

vermelho = (0, 0, 255)
verde = (0, 255, 0)
azul = (255, 0, 0)
am = (0, 255, 255)

# webcam 640x480
# esp 320X240
width=320
height=240
width=width/2
height=height/2

lower_tp = np.array([75,0,60])
#lower_tp = np.array([0,0,0])
upper_tp = np.array([179,116,114])
#upper_tp = np.array([179,150,102])

#lower_tvf = np.array([41,45,0])
#upper_tvf = np.array([91,174,249])
lower_tvf = np.array([33,15,75])
upper_tvf = np.array([76,135,240])

lower_blue = np.array([100, 50, 50]) 
upper_blue = np.array([200, 200,200]) 

board.digital[2].write(1)
board.digital[3].write(1)
board.digital[4].write(1)
board.digital[5].write(1)
board.digital[9].write(1)
board.digital[8].write(1)

center=1

while True:

	board.digital[2].write(0)
	board.digital[3].write(0)
	board.digital[4].write(0)
	board.digital[5].write(0)
	board.digital[9].write(0)
	board.digital[8].write(0)
	if webCamera.isOpened(): 
		camera, frame = webCamera.read()
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#cv2.COLOR_BGR2GRAY)
		hsv = cv2.medianBlur(hsv,5)
		hsv = cv2.inRange(hsv, lower_blue,upper_blue)
		
		detecta = classificadorBolinhaAzul.detectMultiScale(hsv)
		#detecta = classificadorCirculoInterno.detectMultiScale(cinza)
		# print(detecta)
		for(x, y, l, a) in detecta:
			#cv2.rectangle(frame, (x, y), (x + l, y + a), verde, 2)
			cv2.circle(frame, (x+l//2, y+a//2), int((a//2)), azul, 2)
			#cv2.line(frame, (int(width), int(height)), (x+l//2, int(height)), vermelho, 2)
			#cv2.line(frame, (int(width), int(height)), (int(width), y+a//2), vermelho, 2)
			# print("Desligou",l)
			#if l>55:
				#print("Desligou")
				
			
			#print("X",x+l//2,"Y",y+a//2)
			cv2.line(frame, (int((width)), int(height*0.9)), (int((width)), int(height*2)), am, 2)
			cv2.line(frame, (int((width)*1.4), int(height*0.9)), (int((width)*0.6), int(height*0.9)), am, 2)
			cv2.line(frame, (int((width)*1.4), int(height*0.9)), (int(width*1.4), int(0)), am, 2)
			cv2.line(frame, (int((width)*0.6), int(height*0.9)), (int(width*0.6), int(0)), am, 2)
			
			cv2.line(frame, (int(width), int(height)), (x+l//2, int(height)), vermelho, 2)
			cv2.line(frame, (int(width), int(height)), (int(width), y+a//2), vermelho, 2)
			
	
			#print((x+l//2)>=width*0.6 , (x+l//2)<=width*1.4 , (y+a//2)>=height*0.6 , (y+a//2)<=height*1.4 )
			if center==1:
				if ((x+l//2)>=width*0.6 and (x+l//2)<=width*1.4 and (y+a//2)<height*0.9):
					print("REPOUSO ---")
					#AH=50#10 50 130
					
				else:
					if (width-(x+l//2)>=0):
						print("ANTI - HORARIO")
						board.digital[8].write(1)
					else:
						board.digital[9].write(1)
						print("HORARIO")

		
			time.sleep(0.01)
		cv2.imshow("Video WebCamera", frame)
		# time.sleep(0.2)
		if cv2.waitKey(1) == ord('q'):
			break
	else: 
		println("Algo deu errado")


webCamera.release()
cv2.destroyAllWindows()
