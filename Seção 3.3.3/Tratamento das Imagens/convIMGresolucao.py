import os
import cv2
import glob       
import time

base_folder = os.path.dirname(os.path.abspath(__file__))
origin_folder = os.path.join(base_folder, "ImP")
destiny_image_folder = os.path.join(base_folder, "ImPRES")

inicio = time.time()


angles = [0, 180]
count = 0; 
for j in glob.glob(origin_folder+"\*"):
	img =  cv2.imread(j)
	for angle in angles:
		M = cv2.getRotationMatrix2D((img.shape[1] / 2, img.shape[0] / 2), angle, 1)
		image = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))

		gray_image = cv2.resize(image, (0,0),fx=0.05, fy=0.05)
		print(destiny_image_folder+"/framep%d.jpg" % count)
		cv2.imwrite(destiny_image_folder+"/framep%d.jpg" % count, gray_image)    
		count += 1
		gray_image = cv2.resize(image, (0,0),fx=0.1, fy=0.1)
		print(destiny_image_folder+"/framep%d.jpg" % count)
		cv2.imwrite(destiny_image_folder+"/framep%d.jpg" % count, gray_image)    
		count += 1
		gray_image = cv2.resize(image, (0,0),fx=0.2, fy=0.2)
		print(destiny_image_folder+"/framep%d.jpg" % count)
		cv2.imwrite(destiny_image_folder+"/framep%d.jpg" % count, gray_image)    
		count += 1
		gray_image = cv2.resize(image, (0,0),fx=0.4, fy=0.4)
		print(destiny_image_folder+"/framep%d.jpg" % count)
		cv2.imwrite(destiny_image_folder+"/framep%d.jpg" % count, gray_image)    
		count += 1
		
		#gray_image = cv2.resize(image, (0,0),fx=0.025, fy=0.025)
		#print(destiny_image_folder+"/framep%d.jpg" % count)
		#cv2.imwrite(destiny_image_folder+"/framep%d.jpg" % count, gray_image)    
		#count += 1
		gray_image = cv2.resize(image, (0,0),fx=0.0375, fy=0.0375)
		print(destiny_image_folder+"/framep%d.jpg" % count)
		cv2.imwrite(destiny_image_folder+"/framep%d.jpg" % count, gray_image)    
		count += 1

fim = time.time()
print ('duracao: %f' % (fim - inicio))