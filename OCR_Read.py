
from PIL import Image 
from pytesseract import*
import cv2
import time
#import OCRImage as Image
#image.image_func()

def Camera():

    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)
    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 113:            
           # loc_time=time.localtime()
           # Rname=time.strftime("%Y-%m-%d %I:%M:%S %p",loc_time)
           # cv2.imwrite('/home/pi/py-resp/Picture/test.jpg',frame)
            cv2.imwrite('/home/pi/Desktop/Project/Picture/OCRImage.jpg',frame)            
            cv2.destroyWindow("preview")            
            break
                     
        if key == 27: # exit on ESC
            break
        
    #key = cv2.waitKey(20)
    #while(key!= 27):
    display()
    #time.sleep(10)
    #cv2.destroyAllWindow()
    vc.release()
    
    OCR()

    
def display():
    cv2.namedWindow("display")
    img = cv2.imread('/home/pi/Desktop/Project/Picture/OCRImage.jpg')
    cv2.imshow("display",img)
    cv2.waitKey()
    cv2.destroyWindow("display")
    
def OCR():
    print("OCR to txt")
    img0 = Image.open('/home/pi/Desktop/Project/Picture/OCRImage.jpg')
    mychars = image_to_string(img0,'chi_tra').strip()
    print(mychars)
    path = '/home/pi/Desktop/Project/OCR_Output.txt'
    f = open(path, 'w')
    f.write(mychars)
