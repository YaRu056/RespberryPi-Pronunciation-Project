import os
import re
import sys
import tkinter as tk
import OCR_Read as ocr
import txtSpeak as sp
import SpeechRecog as spr
import Comparison as com

#import real_time_test_delete as rt

import cv2
from PIL import  ImageTk,Image, ImageDraw


      
file1 = '/home/pi/Desktop/Project/OCR_Output.txt'
file2 = '/home/pi/Desktop/Project/STT.txt'
global cap
cap=False

def camera_open():
    print("Start")
    global captrue
    captrue = cv2.VideoCapture(0) #開啟相機，0為預設筆電內建相機
    captrue.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) #設置影像參數
    captrue.set(3,600) #像素
    captrue.set(4,800) #像素
#camera_open()
img_viode = '/home/pi/Desktop/Project/Picture/OCRImage1.jpg'    #影像存放位置要改****='/home/pi/Desktop/Project/Picture/OCRImage.jpg'

def openA():
    global s,img_right,label_right,captrue
    ret,frame = captrue.read() #取得相機畫面
    cv2.imwrite(img_viode,frame) #儲存圖片
    img=Image.open(img_viode)
    img_right = ImageTk.PhotoImage(img) #讀取圖片 
    label_right.imgtk=img_right #換圖片
    label_right.config(image=img_right) #換圖片
    s = label_right.after(1, openA) #持續執行open方法，1000為1秒

class basedesk():
    def __init__(self,master):
        self.root = master
        self.root.config()
        self.root.title('Base page')
        #self.root.geometry('200x200')
        #from PIL import  ImageTk, Image, ImageDraw
        self.root.attributes('-fullscreen', True)
 
        Mainpage(self.root)      

        
class Mainpage():
    def __init__(self,master):
        self.master = master
        self.master.config(bg='green')
        #基準介面initface
        self.Mainpage = tk.Frame(self.master,)
        self.Mainpage.pack()
        
        btn_scan = tk.Button(self.Mainpage,text='掃描',font=('標楷體', '40'),command=self.catch)
        btn_scan.pack()
        
        btn_instructions = tk.Button(self.Mainpage,text='說明',font=('標楷體', '40'),command=self.instructions)
        btn_instructions.pack()
        
        btn_exit = tk.Button(self.Mainpage,text='離開',font=('標楷體', '40'),command=self.Exit)
        btn_exit.pack()
        
    def Go_CameraPage(self,):       
        self.Mainpage.destroy()
        #開始拍照 圖片轉文字
        ocr.Camera()
    
        CameraPage(self.master)

    def instructions(self):       
        self.Mainpage.destroy()
        instructions_page(self.master)
        
    def Exit(self):       
        self.master.destroy()
        
    def catch(self):       
        self.Mainpage.destroy()
        CatchPage(self.master)
        
class instructions_page():
    def __init__(self,master):
        self.master = master
        self.master.config(bg='gray')
        self.instructions_page = tk.Frame(self.master,)
        self.instructions_page.pack()
        
        #img= ImageTk.PhotoImage(Image.open('test.jpg'))
        #label_right= tk.Label(self.instructions_page,height=700,width=480,bg ='gray94',fg='blue',image = img) 
        #label_right.grid(row=1,column=0,padx=20, pady=20, sticky="nw") 
        sp.speak1()
        print('test')
        btn_sure = tk.Button(self.instructions_page,text='確定',font=('標楷體', '40'),command=self.Back_mainpage)
        btn_sure.pack()
        
    def Back_mainpage(self,):       
        self.instructions_page.destroy()
        Mainpage(self.master)
        
        
class CatchPage():
    def __init__(self,master):
        camera_open()
        self.master = master
        self.master.config(bg='yellow')
        self.CatchPage = tk.Frame(self.master,)
        self.CatchPage.pack()
        global label_right,button_3
        label_right= tk.Label(self.CatchPage,height=600,width=800,bg ='gray94',fg='blue') 
        #按鈕
        button_1 = tk.Button(self.CatchPage,text = 'catch',bd=4,height=4,width=22,bg ='gray94',command=self.catch)
        button_2 = tk.Button(self.CatchPage,text = 'restart',bd=4,height=4,width=22,bg ='gray94',command =self.restart)
        button_3 = tk.Button(self.CatchPage,text = 'sure',bd=4,height=4,width=22,bg ='gray94',command =self.sure)
        button_3['state']=tk.DISABLED
        button_4 = tk.Button(self.CatchPage,text = 'Exit',bd=4,height=4,width=22,bg ='gray94',command =self.leave)
        
        #位置
        label_right.grid(row=1,column=0,padx=20, pady=20, sticky="nw") 
        button_1.grid(row=1, column=0, padx=100, pady=400, sticky="nw") 
        button_2.grid(row=1, column=0, padx=300, pady=400, sticky="nw")
        button_3.grid(row=1, column=0, padx=500, pady=400, sticky="nw")
        button_4.grid(row=1, column=0, padx=700, pady=400, sticky="nw")
        
        openA()
        
    def catch(self,):
        global img_right,captrue,button_3
        captrue.release() #關閉相機
        label_right.after_cancel(s) #結束拍照
        #label_right.config(image=img) #換圖片
        label_right.imgtk=img_right
        button_3['state']=tk.NORMAL

        
    def restart(self,):
        global button_3
        button_3['state']=tk.DISABLED
        if captrue.isOpened():
            print("I want to close")
        else:
            camera_open()
            openA()
        
    def sure(self,):
        global img_right,captrue
        
        if captrue.isOpened():
            print("I want to stop it")
            captrue.release() #關閉相機
            label_right.after_cancel(s) #結束拍照
        else:
            ocr.OCR()
            self.CatchPage.destroy()
            CameraPage(self.master)
        
    def leave(self):
        global img_right,captrue
        if captrue.isOpened():
            print("bye bye!")
            captrue.release() #關閉相機
            label_right.after_cancel(s) #結束拍照
        self.CatchPage.destroy()
        Mainpage(self.master)

class CameraPage():
    def __init__(self,master):
        self.master = master
        self.master.config(bg='blue')
        self.CameraPage = tk.Frame(self.master,)
        self.CameraPage.pack()
                
        btn_sure = tk.Button(self.CameraPage,text='確定',font=('標楷體', '40'),command=self.Go_ListenPage)
        btn_sure.pack()
        
        btn_leave = tk.Button(self.CameraPage,text='重新拍照',font=('標楷體', '40'),command=self.photo_again)
        btn_leave.pack()
        
        btn_leave = tk.Button(self.CameraPage,text='離開',font=('標楷體', '40'),command=self.leave)
        btn_leave.pack()
        
        #btn_dis = tk.Button(self.CameraPage,text='Display',font=('標楷體', '40'),command=self.ChangeText)
        #btn_dis.pack()
        f=open(file1,"r")
        a=f.read()
        self.text=tk.StringVar()
        self.text.set("Test")
        self.text.set(a)
        print(self.text)
        lb = tk.Label(self.CameraPage,textvariable=self.text ,font=('標楷體', '40'))
        lb.pack()
        
        #lb2= tk.Label(self.CameraPage,height=360,width=480,bg ='gray94',fg='blue',image = img_viode)
        #lb2.pack()
        
    #def ChangeText(self):
        #self.Label["Text"]="Text Updated"
    def leave(self):
        self.CameraPage.destroy()
        Mainpage(self.master)
        
    def photo_again(self):
        #開始拍照 圖片轉文字
        self.CameraPage.destroy()
        CatchPage(self.master)
        #重新拍照
        #self.CameraPage.destroy()
        #Listenpage(self.master)
        print('拍照')
        
    def Go_ListenPage(self,):
        self.CameraPage.destroy()
        #念出圖像中的文字
        OCR=open(file1,'r',encoding="utf-8")
        text1=OCR.read()

        if(text1==""):
            print("No text!")    
        else:
            sp.speak_all()
        ListenPage(self.master)
        
        OCR.close()
        
        
        
        
class ListenPage():
    def __init__(self,master):
        self.master = master
        self.master.config(bg='pink')
        self.ListenPage = tk.Frame(self.master,)
        self.ListenPage.pack()
        
        btn_listen_again = tk.Button(self.ListenPage,text='再聽一次',font=('標楷體', '40'),command=self.listen_again)
        btn_listen_again.pack()
        
        btn_basic = tk.Button(self.ListenPage,text='初級',font=('標楷體', '40'),command=self.Basic)
        btn_basic.pack()
        
        btn_Advance = tk.Button(self.ListenPage,text='進階',font=('標楷體', '40'),command=self.Advance)
        btn_Advance.pack()
        
        btn_back = tk.Button(self.ListenPage,text='離開',font=('標楷體', '40'),command=self.leave)
        btn_back.pack()
        
        btn_back = tk.Button(self.ListenPage,text='上一頁',font=('標楷體', '40'),command=self.back)
        btn_back.pack()
        
    def listen_again(self):
        sp.speak_all()
        
    def Basic(self):
        self.ListenPage.destroy()
        SpeakPage(self.master)
        
    def Advance(self):
        self.ListenPage.destroy()
        SpeakPage(self.master)
    
    def leave(self):
        self.ListenPage.destroy()
        Mainpage(self.master)
        
    def back(self):
        self.ListenPage.destroy()
        CameraPage(self.master)

              
class SpeakPage():
    def __init__(self,master):
        self.master = master
        self.master.config(bg='purple')
        self.SpeakPage = tk.Frame(self.master,)
        self.SpeakPage.pack()
        
        btn_listen_again = tk.Button(self.SpeakPage,text='再聽一次',font=('標楷體', '40'),command=self.listen_again)
        btn_listen_again.pack()
        
        btn_speak_again = tk.Button(self.SpeakPage,text='再念一次',font=('標楷體', '40'),command=self.speak_again)
        btn_speak_again.pack()
        
        btn_score = tk.Button(self.SpeakPage,text='進行評分',font=('標楷體', '40'),command=self.score)
        btn_score.pack()
        
        btn_back = tk.Button(self.SpeakPage,text='離開',font=('標楷體', '40'),command=self.leave)
        btn_back.pack()
        
        btn_back = tk.Button(self.SpeakPage,text='上一頁',font=('標楷體', '40'),command=self.back)
        btn_back.pack()
        
    def listen_again(self):
        sp.speak_all()
        
    def speak_again(self):
        spr.speech_recognition()
        
    def score(self):
        print('進行評分')
        self.SpeakPage.destroy()
        Score(self.master)
        
    def leave(self):
        self.SpeakPage.destroy()
        Mainpage(self.master)
        
    def back(self):
        self.SpeakPage.destroy()
        CameraPage(self.master)
          
    
        
class Score():
    def __init__(self,master):
        self.master = master
        self.master.config(bg='gray')
        self.Score = tk.Frame(self.master,)
        self.Score.pack()
        
        btn_sure = tk.Button(self.Score,text='確定',font=('標楷體', '40'),command=self.Back_ListenPage)
        btn_sure.pack()
        
    def Back_ListenPage(self,):#待設定回哪一個頁面       
        self.Score.destroy()
        ListenPage(self.master)
        
if __name__ == '__main__':    
    root = tk.Tk()
    basedesk(root)
    root.mainloop()
    
'''
#開始拍照 圖片轉文字

while True:
    
    ocr.Camera()
        

    #念出圖像中的文字
    OCR=open(file1,'r',encoding="utf-8")
    text1=OCR.read()

    
    if(text1==""):
        print("No text!")
        
    num =int(input())
    if(num==0):
        break

else:
    sp.speak_all()

#複讀 語音轉文字
spr.speech_recognition()

STT=open(file2,'r',encoding="utf-8")
text2=STT.read()
print(text2)

#比對文字 
com.DisplayScore(text1,text2)
'''
#STT.close()

#OCR.close()








