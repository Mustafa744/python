import numpy as np
import urllib
import cv2
import time
url='http://192.168.1.4:8080/shot.jpg'
lower=np.array([0,0,40])
upper=np.array([180,255,255])
greenlower=np.array([40,50,50])
greenupper=np.array([85,255,255])

def get_image():
    # Use urllib to get the image from the IP camera
    imgResp = urllib.urlopen(url)
    # Numpy to convert into a array
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    # Finally decode the array to OpenCV usable format ;) 
    img = cv2.imdecode(imgNp,-1)
    frame = cv2.imdecode(imgNp,-1)
    return img,frame
height=640
width=480



while 1:

    img,frame =get_image()


    blur=cv2.GaussianBlur(img,(5,5),0)
    hsv=cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,lower,upper)
    mask2=cv2.inRange(hsv,greenlower,greenupper)

    blur2=cv2.GaussianBlur(mask,(5,5),0)#blur the grayscale image
    ret,th1 = cv2.threshold(blur2,35,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)#using threshold remave noise
    ret1,th2 = cv2.threshold(th1,127,255,cv2.THRESH_BINARY_INV)# invert the pixels of the image frame
    
    #contours, hierarchy = cv2.findContours(th2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #find the contours
    widthV=100
    heightV=200
    shiftVX=(width-widthV)/2
    _,contoursV, _= cv2.findContours(th2[heightV:height,shiftVX:shiftVX+widthV],cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    V=_,contoursV, _
    cv2.drawContours(frame[heightV:height,shiftVX:shiftVX+widthV],contoursV,-1,(0,255,0),3)

    heightR=150
    positionRY=0
    shiftRX=shiftVX+widthV
    shiftRY=(height-positionRY-heightR)/2
    _,contoursR, _= cv2.findContours(th2[shiftRY:shiftRY+heightR,shiftRX:width],cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    R=_,contoursR, _
    cv2.drawContours(frame[shiftRY:shiftRY+heightR,shiftRX:width],contoursR,-1,(250,0,0),3)


    heightL=150
    positionLY=0
    shiftLX=0
    shiftLY=(height-positionLY-heightL)/2
    _,contoursL, _= cv2.findContours(th2[shiftLY:shiftLY+heightL,shiftLX:shiftVX],cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    L=_,contoursL, _
    cv2.drawContours(frame[shiftLY:shiftLY+heightL,shiftLX:shiftVX],contoursL,-1,(250,0,0),3)

    


    cv2.line(frame, (shiftVX,0), (shiftVX,680), (212,244,66),2)#y
    cv2.line(frame, (shiftVX+widthV,0), (shiftVX+widthV,680), (212,244,66),2)#y
    cv2.line(frame, (240,0), (240,640), (0,250,255),2)#center
    
    cv2.line(frame, (0,shiftRY), (width,shiftRY), (0,250,255),2)#x
    cv2.line(frame, (0,shiftRY+heightR), (width,shiftRY+heightR), (0,250,255),2)#x
    cv2.line(frame, (0,heightV), (width,heightV), (0,250,255),2)#x

    

    cv2.line(frame, (0,640), (480,640), (0,100,255),30)#x origin remember y inverted
    cv2.circle(frame,(240,630), 5, (0,250,0), -1)
    cv2.circle(frame,(360,630), 5, (0,250,0), -1)
    cv2.circle(frame,(120,630), 5, (0,250,0), -1)


    
    
    
    cv2.imshow('img',img)
    #cv2.imshow("black mask",mask)
    #cv2.imshow("green mask",mask2)


    if V[2] is None:
        print "no line!"
    else:
        for cntV in contoursV:
            area = cv2.contourArea(cntV)# find the area of contour
            if area>=500 :
                # find moment and centroid
                M = cv2.moments(cntV)
                print M
                cx = int(M['m10']/M['m00']+shiftVX)
                cy = int(M['m01']/M['m00']+heightV)
                #print(cx,cy ,"\n")
                cv2.line(frame, (cx,cy), (240,630), (250,0,255),2)
                cv2.circle(frame,(cx,cy), 10, (0,0,255), -1)
                if R[2] is not None:
                    for cntR in contoursR:
                        areaR = cv2.contourArea(cntR)# find the area of contour
                        if areaR>=500 :
                            # find moment and centroid
                            MR = cv2.moments(cntR)
                            cxR = int(MR['m10']/MR['m00']+shiftRX)
                            cyR = int(MR['m01']/MR['m00']+shiftRY)
                            #print(cxR,cyR ,"\n")
                            cv2.line(frame, (cxR,cyR), (360,630), (220,0,220),2)
                            cv2.circle(frame,(cxR,cyR), 5, (0,0,255), -1)

                
                if L[2] is not None:
                    for cntL in contoursL:
                        areaL = cv2.contourArea(cntL)# find the area of contour
                        if areaL>=500 :
                            # find moment and centroid
                            ML = cv2.moments(cntL)
                            cxL = int(ML['m10']/ML['m00']+shiftLX)
                            cyL = int(ML['m01']/ML['m00']+shiftRY)
                            #print(cxL,cyL ,"\n")
                            cv2.line(frame, (cxL,cyL), (120,630), (220,0,220),2)
                            cv2.circle(frame,(cxL,cyL), 5, (0,0,255), -1)

                
                
                MG=cv2.moments(mask2)
                if MG["m00"]>600:
                    cxG = int(MG['m10']/MG['m00'])
                    cyG = int(MG['m01']/MG['m00'])
                    #print(cxx,cyy ,"\n")
                    cv2.line(frame, (cxG,cyG), (240,630), (0,255,0),2)
                    cv2.circle(frame,(cxG,cyG), 10, (0,100,255), -1)
                    #print(cxG,cyG,"\n")
                    if cxG-cx>50 :
                        print "right"
                    elif cxG-cx<-50 :
                        print "left"
                    elif cxG-cx<50 and cxG-cx>-50 :
                        print "B"

                else:
                    print"F"

                





    cv2.imshow('frame',frame) #show video


    
    key=cv2.waitKey(27)
    if key == 27: # exit on ESC
        break
cv2.destroyAllWindows()
exit()

   
