import serial
import time
import serial.tools.list_ports as portlist

ports = list( portlist.comports() )
for p in ports:
  print(p)

def sendSerial(value):
	# try:
		ser=serial.Serial(port="/dev/ttyUSB0",baudrate=115200,timeout=1)
		#ser.flush()
		# ser = serial.Serial()
		# ser.baudrate = 115200
		# ser.port = '/dev/ttyUSB0'
		# ser.timeout=1
		# ser.open()
		#print(ser)
		a="P"
		#print("Sending ",value)
		ser.write(bytes(value, 'UTF-8'))
		#print(ser.readline())
		#ser.flush()
		# ser.write(value.encode())
		ser.close()
	# except:
	# 	print("Porta não encontrada")

#serialPort = serial.Serial(port = "COM4", baudrate=115200,bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

pinE="S,SD100,HA140,FT127,ED197,"
pinD="S,SD100,HA140,FT127,ED57,"
pinC="S,SD197,HA140,FT127,ED127,"
pinB="S,SD100,HA140,FT127,ED127,"
pinR="S,SD120,HA140,FT120,ED120,"

pinF="S,SD100,HA127,FT197,ED197,"
pinT="S,SD100,HA127,FT80,ED57,"
pinH="S,SD197,HA197,FT127,ED127,"
pinA="S,SD100,HA57,FT127,ED127,"
#pinD="S,SD100,HA127,FT127,ED127,"

# Estrutura de mensagem: "S,SD"+str(CB)+",HA"+str(ED)+",FT"+str(FT)+",ED"+str(AH)+","	"++"    "++"
FT=55
CB=110
AH=75
ED=50	

#port="COM3"
#board = pyfirmata.Arduino(port)

import cv2
import numpy as np
#import requests
URL = "http://192.168.3.100:81/stream"
webCamera = cv2.VideoCapture(0)
#webCamera = cv2.VideoCapture(URL)

classificadorCirculoExterno = cv2.CascadeClassifier('Haarcascade/A1.xml')
classificadorCirculoInterno = cv2.CascadeClassifier('Haarcascade/cascade_alvo_central.xml')
classificadorCirculoIntermediario = cv2.CascadeClassifier('Haarcascade/12x12-pos24x24-neg32x24-1500n.xml')
classificadorBolinhaAzul = cv2.CascadeClassifier('Haarcascade/bolinhablk.xml')

vermelho = (0, 0, 255)
verde = (0, 255, 0)
azul = (255, 0, 0)
branco = (255, 255, 255)
preto = (0, 0, 0)

lower_blue = np.array([100, 50, 50]) 
upper_blue = np.array([200, 200,200]) 

state=0

# webcam 640x480
# esp 320X240
width=320
height=240
width=width/2
height=height/2


while True:
	if webCamera.isOpened(): 
		camera, frame = webCamera.read()
		
		cv2.imshow("Video WebCamera", frame)
		tecla=cv2.waitKey(1)
		if tecla == ord('f'):
			FT=FT+1
		if tecla == ord('v'):
			FT=FT-1
		if tecla == ord('g'):
			CB=CB+1
		if tecla == ord('b'):
			CB=CB-1
		if tecla == ord('h'):
			AH=AH+1
		if tecla == ord('n'):
			AH=AH-1
		if tecla == ord('j'):
			ED=ED+1
		if tecla == ord('m'):
			ED=ED-1
		if tecla == ord('k'):
			ED=ED+1
			AH=AH+1
			CB=CB+1
			FT=FT+1
		if tecla == ord(','):
			ED=ED-1
			AH=AH-1
			CB=CB-1
			FT=FT-1
		
		if tecla == ord('1'):
			sendSerial("1")
			time.sleep(1)
		if tecla == ord('2'):
			sendSerial("2")
			time.sleep(1)
		if tecla == ord('3'):
			sendSerial("3")
			time.sleep(1)
		if tecla == ord('4'):
			sendSerial("4")
			time.sleep(1)
		if tecla == ord('5'):
			sendSerial("5")
			time.sleep(1)
		if tecla == ord('6'):
			sendSerial("6")
			time.sleep(1)

		if tecla == ord('p'):
			sendSerial("P")
			time.sleep(1)
		if tecla == ord('i'):
			sendSerial("I")
			time.sleep(1)
		if tecla == ord('d'):
			sendSerial("D")
			time.sleep(1)
		if tecla == ord('e'):
			sendSerial("C")
			time.sleep(1)
		if tecla == ord('r'):
			sendSerial(pinR)
		if tecla == ord('a'):
			state=1
		if tecla == ord('q'):
			break
		print("S,SD"+str(CB)+",HA"+str(ED)+",FT"+str(FT)+",ED"+str(AH)+",")
		sendSerial("S,SD"+str(CB)+",HA"+str(ED)+",FT"+str(FT)+",ED"+str(AH)+",")
	else: 
		print("Algo deu errado")

webCamera.release()
cv2.destroyAllWindows()
