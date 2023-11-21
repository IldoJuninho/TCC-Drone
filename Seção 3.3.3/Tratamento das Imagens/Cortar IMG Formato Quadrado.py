import os
import cv2
import glob       
import time
import re

base_folder = os.path.dirname(os.path.abspath(__file__))
origin_folder = os.path.join(base_folder, "Imagens")
destiny_image_folder = os.path.join(base_folder, "ImP")

inicio = time.time()



count = 0; 
for i in glob.glob(origin_folder+"\*"):  
	gray_image =  cv2.imread(i)[0:240,0:240]# y e x
	#gray_image = cv2.resize(image, (0,0),fx=0.05, fy=0.05)
	value=re.findall(r'\d+',i)
	print(destiny_image_folder+"/framep%d.jpg" % count,value)
	cv2.imwrite(destiny_image_folder+"/framep%d.jpg" % int(value[0]), gray_image)    
	count += 1

fim = time.time()
print ('duracao: %f' % (fim - inicio))
