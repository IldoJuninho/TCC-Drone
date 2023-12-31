import cv2 
import datetime
  

URL = "http://192.168.3.100:81/stream"
video = cv2.VideoCapture(URL) 
   
if (video.isOpened() == False):  
    print("Error reading video file") 
frame_width = int(video.get(3))  
frame_height = int(video.get(4)) 
   
size = (frame_width, frame_height) 
   
result = cv2.VideoWriter("Videos\\"+datetime.datetime.now().strftime("%Y-%m-%d   %H;%M;%S")+'.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         10, size) 
    
while(True): 
    ret, frame = video.read() 
  
    if ret == True:  
      result.write(frame) 
      cv2.imshow('Frame', frame) 
      if cv2.waitKey(1) & 0xFF == ord('s'): 
            break
  
    
    else: 
        break
  
video.release() 
result.release() 
    
cv2.destroyAllWindows() 
   
print("The video was successfully saved") 
