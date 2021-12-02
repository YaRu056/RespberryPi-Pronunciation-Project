#-*- coding: UTF-8 -*-
import tkinter as tk #大小寫要注意,如果小寫不行就改大寫
import time
from PIL import  ImageTk,Image, ImageDraw
import cv2
import random

print("Start")
captrue = cv2.VideoCapture(0) #開啟相機，0為預設筆電內建相機
captrue.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) #設置影像參數
captrue.set(3,350) #像素
captrue.set(4,500) #像素

img_viode = '/home/pi/Desktop/Project/Picture/OCRImage1.jpg'    #影像存放位置 要改


def restart():
    print("Start")
    
    captrue = cv2.VideoCapture(0) #開啟相機，0為預設筆電內建相機
    captrue.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) #設置影像參數
    captrue.set(3,350) #像素
    captrue.set(4,500) #像素
    open()

def open():
    global s,img_right

    ret,frame = captrue.read() #取得相機畫面
    cv2.imwrite(img_viode,frame) #儲存圖片
    img=Image.open(img_viode)
    
    img_right = ImageTk.PhotoImage(img) #讀取圖片 
    label_right.imgtk=img_right #換圖片
    label_right.config(image=img_right) #換圖片
    s = label_right.after(1, open) #持續執行open方法，1000為1秒

    
    

def close():
    captrue.release() #關閉相機
    label_right.after_cancel(s) #結束拍照
    label_right.config(image=img_viode) #換圖片
    
def catch():
    global img_right
    captrue.release() #關閉相機
    label_right.after_cancel(s) #結束拍照
    #label_right.config(image=img) #換圖片
    label_right.imgtk=img_right
    
    

    
    

#創建一個視窗
top = tk.Tk() 
#視窗名稱
top.title('GUI') 
#寬:300高:200的視窗,放在寬:600高:300的位置
top.geometry('600x500+200+100') 

#開啟照片
#img= ImageTk.PhotoImage(Image.open('/home/pi/Desktop/Project/Picture/OCRImage1.jpg')) #要改

#用label來放照片
label_right= tk.Label(top,height=360,width=480,bg ='gray94',fg='blue') 

#按鈕
button_1 = tk.Button(top,text = 'open',bd=4,height=4,width=22,bg ='gray94',command =restart)
button_2 = tk.Button(top,text = 'close',bd=4,height=4,width=22,bg ='gray94',command =close)
button_3 = tk.Button(top,text = 'catch',bd=4,height=4,width=22,bg ='gray94',command =catch)

#位置
label_right.grid(row=1,column=0,padx=20, pady=20, sticky="nw") 
button_1.grid(row=1, column=0, padx=100, pady=400, sticky="nw")  
button_2.grid(row=1, column=0, padx=300, pady=400, sticky="nw")
button_3.grid(row=1, column=0, padx=500, pady=400, sticky="nw")

open()

top.mainloop() #執行視窗


'''
def check():
    global captrue
    if captrue.isOpened(): #判斷相機是否有開啟
        open()
    else:
        captrue = cv2.VideoCapture(0) 
        captrue.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) #設置影像參數
        captrue.set(3,350) #像素
        captrue.set(4,500) #像素
        open()
        
'''


'''
if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False
        

cv2.namedWindow("preview")
if capture.isOpened(): # try to get the first frame
    rval, frame = capture.read()
else:
    rval = False

while rval:
    print("Good")
    cv2.imshow("preview", frame)
    rval, frame = capture.read()
    time.sleep(5)
    capture.release()
    break
    
print("Picture")'''