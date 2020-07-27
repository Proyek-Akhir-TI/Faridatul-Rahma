import numpy as np
import cv2

cam = cv2.VideoCapture(0)

while True:
    ret,frame = cam.read()
#    frame = cv2.flip(frame,1)
  #  frame = cv2.rotate(frame, cv2.ROTATE_180)
    
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #definig the range of red color
    red_lower=np.array([103, 125, 130],np.uint8) #103, 125, 130
    red_upper=np.array([255,255,255],np.uint8)

    #defining the Range of green color
    green_lower=np.array([64, 120, 51],np.uint8)
    green_upper=np.array([169,255,255],np.uint8)
    
    red=cv2.inRange(hsv, red_lower, red_upper)
    green=cv2.inRange(hsv,green_lower,green_upper)
    
    #Morphological transformation, Dilation     
    kernal = np.ones((3 ,3), "uint8")

    red=cv2.dilate(red, kernal)
    res=cv2.bitwise_and(frame, frame, mask = red)

    green=cv2.dilate(green,kernal)
    res1=cv2.bitwise_and(frame, frame, mask = green)
    
    blur = cv2.medianBlur(gray,5)
    circles = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,1.5,10)
    
    try:
        
        for i in circles[0,:]:
            cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
            cv2.circle(frame,(i[0],i[1]),2,(0,0,255),5)
            #cv2.putText(frame,str(len(circles[0])-1), (10,50),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,0),2)
        
            #Tracking the Red Color
            contours, _=cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area>200):
            
                    x,y,w,h = cv2.boundingRect(contour) 
                    frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(38,11,208),2)
                    #cv2.putText(frame,"RED",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (38,11,208))
                    cv2.putText(frame,"merah", (x,y),cv2.FONT_HERSHEY_COMPLEX,1,(38,11,208),2, cv2.LINE_AA)
                    
            #Tracking the Green Color
            contours, _=cv2.findContours(green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area>200):
                    x,y,w,h = cv2.boundingRect(contour) 
                    frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(33,103,67),2)
                    #cv2.putText(frame,"Green",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (33,103,67))
                    cv2.putText(frame,"hijau", (x,y),cv2.FONT_HERSHEY_COMPLEX,1,(33,103,67),2, cv2.LINE_AA)
                    
        cv2.imshow('Detected Circle', frame)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
            
    except:
        
        cv2.imshow('No Circle', frame)
        
cam.release()
cv2.destroyAllWindows()
