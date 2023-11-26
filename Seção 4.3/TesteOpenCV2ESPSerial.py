import serial
import time
import serial.tools.list_ports as portlist
import datetime
import threading

ports = list( portlist.comports() )
for p in ports:
  print(p)

ser=serial.Serial(port="/dev/ttyUSB0",baudrate=115200,timeout=.001)

def sendSerial(value):
	# try:
		# ser=serial.Serial(port="/dev/ttyUSB0",baudrate=115200,timeout=1)
		global ser
		#ser.flush()
		# ser = serial.Serial()
		# ser.baudrate = 115200
		# ser.port = '/dev/ttyUSB0'
		# ser.timeout=1
		# ser.open()
		# print(ser)
		# a="P"
		# print("Sending ",value)
		ser.write(bytes(value, 'UTF-8'))
		ser.readlines()
		#print(ser.readline())
		#ser.flush()
		# ser.write(value.encode())
		# ser.close()
	# except:
	# 	print("Porta não encontrada")

#serialPort = serial.Serial(port = "COM4", baudrate=115200,bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

pinE="S,SD120,HA70,FT70,ED130,"
pinD="S,SD120,HA70,FT70,ED10,"
pinC="S,SD160,HA70,FT70,ED50," #170
pinB1="S,SD72,HA70,FT70,ED50," #72
pinB="S,SD95,HA70,FT70,ED50,"
pinR="S,SD120,HA70,FT70,ED50,"

pinF="S,SD120,HA70,FT178,ED50," 
pinT="S,SD120,HA70,FT0,ED50,"#42
pinH="S,SD120,HA178,FT70,ED50,"
pinA="S,SD120,HA42,FT70,ED50,"
#pinD="S,SD100,HA127,FT127,ED127,"

# Estrutura de mensagem: "S,SD"+str(CB)+",HA"+str(ED)+",FT"+str(FT)+",ED"+str(AH)+","	"++"    "++"
FT=44 #70
CB=118 #120
AH=50		
ED=75 # 

# ESQ=178 DIR=42 FRE=170 TRA=20
ESQ=104
DIR=38
FRE=105
TRA=44

#port="COM3"
#board = pyfirmata.Arduino(port)

import cv2
import numpy as np
#import requests
URL = "http://192.168.3.100:81/stream"
#webCamera = cv2.VideoCapture(0)
webCamera = cv2.VideoCapture(URL)

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

lower_tvf = np.array([41,45,0])
upper_tvf = np.array([91,174,249])

lower_tp = np.array([86,36,28])
upper_tp = np.array([179,150,102])
state=0


frame_width = int(webCamera.get(3)) 
frame_height = int(webCamera.get(4)) 
   
size = (frame_width, frame_height)
result = cv2.VideoWriter("Videos//"+datetime.datetime.now().strftime("%Y-%m-%d   %H;%M;%S")+'.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         10, size) 

comantED=0
comantFT=0
# webcam 640x480
# esp 320X240
# width=320*2
# height=240*2
width=320
height=240
width=width/2
height=height/2



t1=time.monotonic()
t2=time.monotonic()
t3=time.monotonic()
t4=time.monotonic()
t5=time.monotonic()


def ProcessImBolV(frame):
	global comantFT,comantED
	global ED,FT,CB,AH
	global t1,state
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#cv2.COLOR_BGR2GRAY)
	hsv = cv2.medianBlur(hsv,5)
	hsv = cv2.inRange(hsv, lower_tvf,upper_tvf)
	detecta = classificadorBolinhaAzul.detectMultiScale(hsv)
	#detecta = classificadorCirculoInterno.detectMultiScale(cinza)
	# print(detecta)
	for(x, y, l, a) in detecta:
		#cv2.rectangle(frame, (x, y), (x + l, y + a), verde, 2)
		cv2.circle(frame, (x+l//2, y+a//2), int((a//2)), verde, 2)
		cv2.line(frame, (int(width), int(height)), (x+l//2, int(height)), vermelho, 2)
		cv2.line(frame, (int(width), int(height)), (int(width), y+a//2), vermelho, 2)
		# print(l)
		if l>65: #65 verde
			print("Desligou")
			sendSerial("f")
			time.sleep(0.12)
			sendSerial("D")
			state=0
			time.sleep(3)
			print("Tempo de pouso",time.monotonic()-t1)
			sendSerial("D")
			sendSerial("D")
			time.sleep(5)
		# print(width+width*0.3,width-width*0.3,height+height*0.4,height-height*0.4)

		# cv2.line(frame, (int(width*2), int(height)), (int(width), int(height+height*0.4)), verde, 2)
		# cv2.line(frame, (int(width*2), int(height)), (int(width), int(height-height*0.4)), verde, 2)
		# cv2.line(frame, (int(width*2), int(height*2)), (int(width+width*0.3), int(height)), azul, 2)
		# cv2.line(frame, (int(width*2), int(height*2)), (int(width-width*0.3), int(height)), azul, 2)
		
		# if ((x+l//2)-width*0.7>=0 and (x+l//2)-width*1.3<=0 and (y+a//2)-height*0.7>=0 and (y+a//2)-height*1.3<=0 ):#ED 75 42 178 CB 60 20T 170F
		# 	print("TDescendo")
		# 	CB=95
		# 	center=1
		# else:
		print((x+l//2),(y+a//2))
		if (width-(x+l//2)<=0):
			# sendSerial(pinH)
			if (x+l//2)>=208:
				ED=ESQ 
				print("ESQ")
				comantED=1
			else:
				if comantED==1:
					comantED=0
					ED=DIR

		else:
			if (x+l//2)<=112:
				ED=DIR
				print("DIR")
				comantED=1
			else:
				if comantED==1:
					comantED=0
					ED=ESQ
			# sendSerial(pinA)

		if (height-(y+a//2)<=0):
			#board.digital[5].write(1)
			# sendSerial(pinT)
			if (y+a//2)>=168:
				FT=FRE
				print("FRE")
				comantFT=1
			else:
				if comantFT==1:
					comantFT=0
					FT=TRA
		else:
			if (y+a//2)<=72:
				FT=TRA
				print("TRA")
				comantFT=1
			else:
				if comantFT==1:
					comantFT=0
					FT=FRE	
			# sendSerial(pinF)
			# sendSerial(pinA)
			# print("DIR")

		# if (height-(y+a//2))>=0:
		# 	#board.digital[5].write(1)
		# 	sendSerial(pinT)
		# 	print("BAIXO")
		# else:
		# 	sendSerial(pinF)
		# 	print("CIM")






def ProcessImBolA(frame):
	global comantFT
	global comantED
	global t1,state
	global ED,FT,CB,AH
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#cv2.COLOR_BGR2GRAY)
	hsv = cv2.medianBlur(hsv,5)
	hsv = cv2.inRange(hsv, lower_blue,upper_blue)
	detecta = classificadorBolinhaAzul.detectMultiScale(hsv)
	for(x, y, l, a) in detecta:
		#cv2.rectangle(frame, (x, y), (x + l, y + a), verde, 2)
		cv2.circle(frame, (x+l//2, y+a//2), int((a//2)), azul, 2)
		#cv2.line(frame, (int(width), int(height)), (x+l//2, int(height)), vermelho, 2)
		#cv2.line(frame, (int(width), int(height)), (int(width), y+a//2), vermelho, 2)
		# print("Desligou",l)
		if l>55:
			print("Desligou")
			sendSerial("f")
			time.sleep(0.12)
			sendSerial("D")
			state=0
			time.sleep(3)
			print("Tempo de pouso",time.monotonic()-t1)
			sendSerial("D")
			sendSerial("D")
			time.sleep(5)
		
		#print("X",x+l//2,"Y",y+a//2)

		#print((x+l//2)>=width*0.6 , (x+l//2)<=width*1.4 , (y+a//2)>=height*0.6 , (y+a//2)<=height*1.4 )
		if center==1:
			if ((x+l//2)>=width*0.6 and (x+l//2)<=width*1.4 and (y+a//2)>=height*0.6):
				print("REPOUSO ---")
				AH=50#10 50 130
				
			else:
				if (width-(x+l//2)>=0):
					print("HORARIO")
					AH=10
				else:
					print("ANTI - HORARIO")
					AH=130

			


threadCircle = threading.Thread()
threadBB = threading.Thread()
threadCircle.start()
threadBB.start()


while True:
	if webCamera.isOpened(): 
		camera, frame = webCamera.read()
		FT=44 #70
		CB=118 #120
		AH=50
		ED=75 # 70

		#t1=time.monotonic()
		cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
		center=0
		
		if state==3:
			threadCircle = threading.Thread(target=ProcessImBolV, args=(frame,))
			threadCircle.start()


		if state==2:
			detecta = classificadorCirculoIntermediario.detectMultiScale(cinza)
			print(detecta)
			try:
				print("Max",max(detecta[:][2]))
			except:
				p=0
			for(x, y, l, a) in detecta:
				#cv2.rectangle(frame, (x, y), (x + l, y + a), verde, 2)
				cv2.circle(frame, (x+l//2, y+a//2), int((a//2)), branco, 2)
				cv2.line(frame, (int(width), int(height)), (x+l//2, int(height)), vermelho, 2)
				cv2.line(frame, (int(width), int(height)), (int(width), y+a//2), vermelho, 2)
				print(l)
				if l>170:
					print("Trocou o estado")
					state=3
				
				if ((x+l//2)-width*0.8>=0 and (x+l//2)-width*1.2<=0 and (y+a//2)-height*0.8>=0 and (y+a//2)-height*1.2<=0 ):#ED 75 42 178 CB 60 20T 170F
					print("TDescendo")
				else:
					if (width-(x+l//2))>=0:
						# sendSerial(pinH)
						ED=42
						print("ESQ")
					else:
						# sendSerial(pinA)
						ED=178
						print("DIR")

					if (height-(y+a//2))>=0:
						#board.digital[5].write(1)
						# sendSerial(pinT)
						FT=20
						print("BAIXO")
					else:
						# sendSerial(pinF)
						FT=170
						print("CIM")
				# if (width-(x+l//2))>=0:
				# 	sendSerial(pinH)
				# 	print("ESQ")
				# else:
				# 	sendSerial(pinA)
				# 	print("DIR")

				# if (height-(y+a//2))>=0:
				# 	#board.digital[5].write(1)
				# 	sendSerial(pinT)
				# 	print("BAIXO")
				# else:
				# 	sendSerial(pinF)
				# 	print("CIM")

		if state==1:
			detecta = classificadorCirculoExterno.detectMultiScale(cinza)
			# print(detecta)
			# try:
			# 	print("Max",max(detecta[:][2]))
			# except:
			# 	p=0
			for(x, y, l, a) in detecta:
				#cv2.rectangle(frame, (x, y), (x + l, y + a), verde, 2)
				cv2.circle(frame, (x+l//2, y+a//2), int((a//2)), preto, 2)
				cv2.line(frame, (int(width), int(height)), (x+l//2, int(height)), vermelho, 2)
				cv2.line(frame, (int(width), int(height)), (int(width), y+a//2), vermelho, 2)
				# sendSerial("S,SD"+str(CB)+",HA"+str(ED)+",FT"+str(FT)+",ED"+str(AH)+",")
				print(l)
				if l>200:
					print("Trocou o estado")
					# state=3
				
				if ((x+l//2)-width*0.9>=0 and (x+l//2)-width*1.1<=0 and (y+a//2)-height*0.9>=0 and (y+a//2)-height*1.1<=0 ):#ED 75 42 178 CB 60 20T 170F
					print("TDescendo")
				else:
					if (width-(x+l//2))>=0:
						# sendSerial(pinH)
						ED=ESQ 
						print("ESQ")
					else:
						ED=DIR
						print("DIR")
						# sendSerial(pinA)

					if (height-(y+a//2))>=0:
						#board.digital[5].write(1)
						# sendSerial(pinT)
						FT=FRE
						print("CIM")
					else:
						FT=TRA
						print("BAIXO")
				
				
				# if (width-(x+l//2))>=0:
				# 	sendSerial(pinH)
				# 	# print("ESQ")

				# else:
				# 	sendSerial(pinA)
				# 	# print("DIR")

				# if (height-(y+a//2))>=0:
				# 	#board.digital[5].write(1)
				# 	sendSerial(pinT)
				# 	# print("BAIXO")
				# else:
				# 	sendSerial(pinF)
					# print("CIM")
		
		
		#print("Delay Pross",time.monotonic()-t1)

		# detecta = classificadorVideoFace.detectMultiScale(cinza)
		# #print(frame.shape[1])
		# #print(camera.shape[0])
		# for(x, y, l, a) in detecta:
		# 	cv2.rectangle(frame, (x, y), (x + l, y + a), (255, 0, 0), 2)
		# 	cv2.line(frame, (int(width), int(height)), (x+l//2, int(height)), vermelho, 1)
		# 	cv2.line(frame, (int(width), int(height)), (int(width), y+a//2), verde, 1)
		# 	#cv2.line(frame, (x, 240), (320, 240), vermelho, 1)
		# 	#cv2.line(frame, (320, y), (320, 240), verde, 1)
		# 	#cv2.line(frame, (180, 120), (x+l//2, 120), verde, 1)
		# 	#cv2.line(frame, (0, 0), (320, 240), verde, 1)
		# 	#print(x, l)
		# 	#print(frame.shape[1])
		# 	#print(frame.shape[0])

		# 	if (width-(x+l//2))>=0:
		# 		#board.digital[2].write(1)
		# 		#board.digital[3].write(0)
		# 		print("ESQ")
		# 	else:
		# 		#board.digital[2].write(0)
		# 		#board.digital[3].write(1)
		# 		print("DIR")

		# 	if (height-(y+a//2))>=0:
		# 		#board.digital[5].write(1)
		# 		#board.digital[4].write(0)
		# 		print("BAIXO")
		# 	else:
		# 		#board.digital[5].write(0)
		# 		#board.digital[4].write(1)
		# 		print("CIM")
		# 	# sendSerial(pinD)		

		# 	#pegaOlho = frame[y:y + a, x:x + l]
		# 	#OlhoCinza = cv2.cvtColor(pegaOlho, cv2.COLOR_BGR2GRAY)
		# 	#localizaOlho = classificadorOlho.detectMultiScale(OlhoCinza)
		# 	#for (ox, oy, ol, oa) in localizaOlho:
		# 		#cv2.rectangle(pegaOlho, (ox, oy), (ox + ol, oy + oa), (0, 255, 0), 2)

# print(state)
		if state>1 and state<=3:
			threadBB = threading.Thread(target=ProcessImBolA, args=(frame,))
			threadBB.start()
		# print(CB,ED,FT,AH)


		# threadBB.join()
		# threadCircle.join()

		frame =  cv2.flip(frame, -1) # Apenas esp32
		cv2.imshow("Video WebCamera", frame)
		tecla=cv2.waitKey(1)
		if tecla == ord('y'):
			sendSerial(pinC)
			time.sleep(0.02)
			sendSerial("s")
		if tecla == ord('h'):
			sendSerial(pinB)
		if tecla == ord('g'):
			sendSerial(pinE)
		if tecla == ord('j'):
			sendSerial(pinD)
		if tecla == ord('s'):
			sendSerial(pinF)
		if tecla == ord('x'):
			sendSerial(pinT)
		if tecla == ord('z'):
			sendSerial(pinH)
		if tecla == ord('c'):
			sendSerial(pinA)
		if tecla == ord('n'):
			sendSerial(pinB1)
		if tecla == ord('p'):
			sendSerial("P")
		if tecla == ord('i'):
			sendSerial("I")
		if tecla == ord('d'):
			print("Tempo de pouso",time.monotonic()-t1)
			sendSerial("D")
			time.sleep(3)
			print("Tempo de pouso",time.monotonic()-t1)
			print("Delay Captura",time.monotonic()-t3)
		if tecla == ord('e'):
			sendSerial("C")
		if tecla == ord('w'):
			state=0
		if tecla == ord('r'):
			sendSerial(pinR)
		if tecla == ord('a'):
			t1=time.monotonic()
			state=0
			sendSerial("d")
		if tecla == ord('v'):
			sendSerial("f")
			t3=time.monotonic()
		if tecla == ord('q'):
			break
		# if tecla==-1:
		# 	if (state>0):
		# 		sendSerial("S,SD"+str(CB)+",HA"+str(ED)+",FT"+str(FT)+",ED"+str(AH)+",")

		result.write(frame)
	else: 
		print("Algo deu errado")

webCamera.release()
cv2.destroyAllWindows()
