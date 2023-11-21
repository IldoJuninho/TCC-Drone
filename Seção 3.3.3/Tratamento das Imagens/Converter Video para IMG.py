import os
import cv2
import glob       
import time

base_folder = os.path.dirname(os.path.abspath(__file__))
origin_folder = os.path.join(base_folder, "Videos")
destiny_image_folder = os.path.join(base_folder, "Imagens")

inicio = time.time()



count = 0; 
for i in glob.glob(origin_folder+"\*"):      
	vidcap = cv2.VideoCapture(i)
	success,image = vidcap.read()
	while success:
		success,image = vidcap.read()
		if success:
			#Converte a img para escala de cinza
			gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
			print(destiny_image_folder+"/framep%d.jpg" % count)
			cv2.imwrite(destiny_image_folder+"/framep%d.jpg" % count, gray_image)    
		count += 1

fim = time.time()
print ('duracao: %f' % (fim - inicio))
