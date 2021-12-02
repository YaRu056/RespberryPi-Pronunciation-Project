#-*- coding: UTF-8 -*-
import tkinter as tk #大小寫要注意,如果小寫不行就改大寫
import time
from PIL import  ImageTk,Image, ImageDraw
import cv2
import random

def camera():
    print("Start")
    global captrue
    captrue = cv2.VideoCapture(0) #開啟相機，0為預設筆電內建相機
    captrue.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) #設置影像參數
    captrue.set(3,350) #像素
    captrue.set(4,500) #像素

camera()

img_viode = '/home/pi/Desktop/Project/Picture/OCRImage1.jpg'    #影像存放位置 要改



def restart():
    camera()
    openA()

def openA():
    global s,img_right,captrue

    ret,frame = captrue.read() #取得相機畫面
    cv2.imwrite(img_viode,frame) #儲存圖片
    img=Image.open(img_viode)
    
    img_right = ImageTk.PhotoImage(img) #讀取圖片 
    label_right.imgtk=img_right #換圖片
    label_right.config(image=img_right) #換圖片
    s = label_right.after(1, openA) #持續執行open方法，1000為1秒

    
    

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

openA()

top.mainloop() #執行視窗


