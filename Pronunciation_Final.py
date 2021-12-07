import os
import re
import sys
import tkinter as tk
import OCR_Read as ocr
import txtSpeak as sp
import SpeechRecog as spr
import Score as score
from tkinter import *
import cv2
from PIL import  ImageTk,Image, ImageDraw


      
file1 = '/home/pi/Desktop/Project/OCR_Output.txt'
file2 = '/home/pi/Desktop/Project/STT.txt'



def BG(width,height,frame,path):
    BGwidth=1920
    BGheight=1080
    img=Image.open(path)
    img=img.resize((width,height),Image.ANTIALIAS)
    
    BGImg=ImageTk.PhotoImage(img)
    
    Background = tk.Label(frame,image=BGImg,width=width)
    Background.image=BGImg
    return Background

def btn_img(frame,width,height,path,com):
    
    img=Image.open(path)
    img=img.resize((width,height),Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)
    b=tk.Button(frame,text='',image=photo,bd=0,command=com)
    b.image=photo
   
    return b

def camera_open():
    print("Start")
    global captrue
    captrue = cv2.VideoCapture(0) #開啟相機，0為預設筆電內建相機
    captrue.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) #設置影像參數
    captrue.set(3,600) #像素
    captrue.set(4,800) #像素

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
        
        
        #基準介面initface
        
        self.Mainpage = tk.Frame(self.master,)
        self.Mainpage.place(x=0,y=0)
        img_BG='/home/pi/Desktop/Project/Picture/BG.png'
        MainBG=BG(1920,1080,self.Mainpage, img_BG)
        MainBG.place(x=0,y=0)
        #print(type(MainBG))
        img_scan='/home/pi/Desktop/Project/Picture/Mscan_Btn.png'
        img_ins='/home/pi/Desktop/Project/Picture/Muse_Btn.png'
        img_exit='/home/pi/Desktop/Project/Picture/Mexit_Btn.png'
                
        btn_scan = btn_img(self.Mainpage,300,150,img_scan,self.catch)
        btn_instructions = btn_img(self.Mainpage,300,150,img_ins,self.instructions)
        btn_exit = btn_img(self.Mainpage,300,150,img_exit,self.Exit)

        btn_t = tk.Label(self.Mainpage,text='',font=('標楷體', '40'),bg='#FBE5D6')
        btn_e = tk.Label(self.Mainpage,text='',font=('標楷體', '40'),bg='#FBE5D6')
        #位置.
        
        btn_t.grid(row=0,column=0, padx=200, pady=100, sticky="nw")
        btn_e.grid(row=1,column=0, padx=200, pady=100, sticky="nw")
        btn_scan.grid(row=2, padx=500, pady=200, sticky="nw")
        btn_instructions.grid(row=2,padx=850, pady=200, sticky="nw")
        btn_exit.grid(row=2,padx=1200, pady=200, sticky="nw")

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
        self.instructions_page.place(x=0,y=0)
        img_BG='/home/pi/Desktop/Project/Picture/Ins.png'
        InsBG=BG(1920,1080,self.instructions_page, img_BG)
        InsBG.place(x=0,y=0)
        sp.speak1()
        #print('test')
        #按鈕標籤
        img_sure='/home/pi/Desktop/Project/Picture/Usure_Btn.png'
        img_lis='/home/pi/Desktop/Project/Picture/Ulis_Btn.png'

        btn_sure = btn_img(self.instructions_page,300,150,img_sure,self.Back_mainpage)
        btn_listen =btn_img(self.instructions_page,300,150,img_lis,self.Listen)
        btn_t = tk.Label(self.instructions_page,text='',font=('標楷體', '40'),bg='black')
        btn_e = tk.Label(self.instructions_page,text='',font=('標楷體', '40'),bg='black')
        #位置
        btn_t.grid(row=0,column=0, padx=200, pady=200, sticky="nw")
        btn_e.grid(row=1,column=0, padx=200, pady=120, sticky="nw")
        btn_sure.grid(row=2, padx=600, pady=80, sticky="nw")
        btn_listen.grid(row=2, padx=1000, pady=80, sticky="nw")
       

    def Back_mainpage(self,):       
        self.instructions_page.destroy()
        Mainpage(self.master)
        
    def Listen(self,):
        sp.speak1()
        
        
class CatchPage():
    def __init__(self,master):
        camera_open()
        self.master = master
        self.CatchPage = tk.Frame(self.master,)
        self.CatchPage.place(x=0,y=0)
        print("Catch")
        img_BG='/home/pi/Desktop/Project/Picture/CatchBG.png'
        
        CatchBG=BG(1920,1080,self.CatchPage, img_BG)
        CatchBG.place(x=0,y=0)
        global label_right,button_3,lb
        label_right= tk.Label(self.CatchPage,height=500,width=670,bg='black',fg='blue')
        img_pic='/home/pi/Desktop/Project/Picture/Cpic_Btn.png'
        img_redo='/home/pi/Desktop/Project/Picture/Credo_Btn.png'
        img_sure='/home/pi/Desktop/Project/Picture/Csure_Btn.png'
        img_exit='/home/pi/Desktop/Project/Picture/Cexit_Btn.png'

        button_1 =btn_img(self.CatchPage,300,150,img_pic,self.catch)
        button_2 =btn_img(self.CatchPage,300,150,img_redo,self.restart)
        button_3 =btn_img(self.CatchPage,300,150,img_sure,self.sure)
        button_3['state']=tk.DISABLED
        button_4 =btn_img(self.CatchPage,300,150,img_exit,self.leave)
        btn_t = tk.Label(self.CatchPage,text='',bg='#DAE3F3')
        lb = tk.Label(self.CatchPage ,font=('標楷體', '40'))
        lb.grid(row=2,padx=0, pady=100 ,sticky="nw")
        #位置
        btn_t.grid(row=3,column=0, padx=180, pady=100, sticky="nw")
        #btn_e.grid(row=1,column=0, padx=200, pady=100, sticky="nw")
        label_right.grid(row=0,column=0,padx=629, pady=150,rowspan=2 ,sticky="nw")
        
        button_1.grid(row=2, padx=350, pady=50, sticky="nw") 
        button_2.grid(row=2, padx=700, pady=50, sticky="nw")
        button_3.grid(row=2, padx=1050, pady=50, sticky="nw")
        button_4.grid(row=2,padx=1400, pady=50, sticky="nw")
        
        openA()
        
    def catch(self,):
        global img_right,captrue,button_3,lb
        captrue.release() #關閉相機
        label_right.after_cancel(s) #結束拍照
        #label_right.config(image=img) #換圖片
        label_right.imgtk=img_right
        button_3['state']=tk.NORMAL
        f=open(file1,"r")
        a=f.read()
        self.text=tk.StringVar()
        self.text.set("Test")
        self.text.set(a)
        lb.textvariable=self.text
        print(self.text)
        
        f.close()
        
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
            #念出圖像中的文字
            OCR=open(file1,'r',encoding="utf-8")
            text1=OCR.read()
            if(text1==""):
                print("No text!")    
            else:
                sp.speak_all()
            ListenPage(self.master)
            
            OCR.close()
        
    def leave(self):
        global img_right,captrue
        if captrue.isOpened():
            print("bye bye!")
            captrue.release() #關閉相機
            label_right.after_cancel(s) #結束拍照
        self.CatchPage.destroy()
        Mainpage(self.master)
        
class ListenPage():
    def __init__(self,master):
        self.master = master
        
        self.ListenPage = tk.Frame(self.master,)
        self.ListenPage.place(x=0,y=0)
        img_BG='/home/pi/Desktop/Project/Picture/ListenBG.png'
        MainBG=BG(1920,1080,self.ListenPage, img_BG)
        MainBG.place(x=0,y=0)
        #按鈕標籤
        img_lis='/home/pi/Desktop/Project/Picture/Llis_Btn.png'
        img_goR='/home/pi/Desktop/Project/Picture/Lgo_Btn.png'
        img_redo='/home/pi/Desktop/Project/Picture/Lredo_Btn.png'
        img_exit='/home/pi/Desktop/Project/Picture/Lexit_Btn.png'

        btn_listen_again=btn_img(self.ListenPage,300,150,img_lis,self.listen_again)
        btn_basic=btn_img(self.ListenPage,300,150,img_goR,self.Basic)
        btn_back =btn_img(self.ListenPage,300,150,img_redo,self.back)
        btn_exit =btn_img(self.ListenPage,300,150,img_exit,self.leave)  
        btn_t = tk.Label(self.ListenPage,text='',font=('標楷體', '40'),bg='#DFEBE9')
       
        #位置.
        
        btn_t.grid(row=0,column=0, padx=200, pady=350, sticky="nw")
       
        #位置
        btn_listen_again.grid(row=1,padx=350, pady=100, sticky="nw") 
        btn_basic.grid(row=1, padx=700, pady=100, sticky="nw")
        btn_back.grid(row=1, padx=1050, pady=100, sticky="nw")
        btn_exit.grid(row=1,  padx=1400, pady=100, sticky="nw")
        
    def listen_again(self):
        sp.speak_all()
        
    def Basic(self):
        self.ListenPage.destroy()
        SpeakPage(self.master)
    
    def leave(self):
        self.ListenPage.destroy()
        Mainpage(self.master)
        
    def back(self):
        self.ListenPage.destroy()
        CatchPage(self.master)#!!!!!!!!!!!!

              
class SpeakPage():
    def __init__(self,master):
        self.master = master
        
        self.SpeakPage = tk.Frame(self.master,)
        self.SpeakPage.place(x=0,y=0)
        img_BG='/home/pi/Desktop/Project/Picture/RepeatBG.png'
        MainBG=BG(1920,1080,self.SpeakPage, img_BG)
        MainBG.place(x=0,y=0)
        #按鈕標籤
        img_lis='/home/pi/Desktop/Project/Picture/Slis_Btn.png'
        img_repeat='/home/pi/Desktop/Project/Picture/Srepeat_Btn.png'
        img_score='/home/pi/Desktop/Project/Picture/Sscore_Btn.png'
        img_redo='/home/pi/Desktop/Project/Picture/Sredo_Btn.png'
        img_exit='/home/pi/Desktop/Project/Picture/Sexit_Btn.png'

        btn_listen_again =btn_img(self.SpeakPage,300,150,img_lis,self.listen_again)
        btn_speak_again=btn_img(self.SpeakPage,300,150,img_repeat,self.speak_again)
        btn_score=btn_img(self.SpeakPage,300,150,img_score,self.score)
        btn_exit=btn_img(self.SpeakPage,300,150,img_exit,self.leave)
        btn_back=btn_img(self.SpeakPage,300,150,img_redo,self.back)

        btn_t = tk.Label(self.SpeakPage,text='',font=('標楷體', '30'),bg='#BED5DB')
       
        #位置.
        
        btn_t.grid(row=0,column=0, padx=200, pady=350, sticky="nw")
        
        #位置
       
        btn_listen_again.grid(row=1, padx=200, pady=100, sticky="nw") 
        btn_speak_again.grid(row=1, padx=550, pady=100, sticky="nw")
        btn_score.grid(row=1, padx=900, pady=100, sticky="nw")
        btn_back.grid(row=1, padx=1250, pady=100, sticky="nw")
        btn_exit.grid(row=1, padx=1600, pady=100, sticky="nw")
        '''
        global lb0
        self.text=tk.StringVar()
        self.text.set(" ")

        lb0 = tk.Label(self.SpeakPage,textvariable=self.text ,font=('microsoft yahei', '30'),bg='white')
        lb0.grid(row=0, padx=1400, pady=300, sticky="nw")


    def display():
        global lb0
        STT=open(file2,'r',encoding="utf-8")
        text2=STT.read()
        self.text=tk.StringVar()
        self.text.set(text2)
        lb0.textvariable=self.text
'''

    def listen_again(self):
        sp.speak_all()
        
    def speak_again(self):
        spr.speech_recognition()
        #display()
        
    def score(self):
        print('進行評分')
        self.SpeakPage.destroy()
        Score(self.master)
        
    def leave(self):
        self.SpeakPage.destroy()
        Mainpage(self.master)
        
    def back(self):
        self.SpeakPage.destroy()
        CatchPage(self.master)
          
    
        
class Score():
    def __init__(self,master):
        self.master = master
        
        self.Score = tk.Frame(self.master,)
        self.Score.place(x=0,y=0)
        img_BG='/home/pi/Desktop/Project/Picture/ScoreBG.png'
        MainBG=BG(1920,1080,self.Score, img_BG)
        MainBG.place(x=0,y=0)
        OCR=open(file1,'r',encoding="utf-8")
        text1=OCR.read()
        STT=open(file2,'r',encoding="utf-8")
        text2=STT.read()
        s=score.Display_Score(text1,text2)+"%"
        STT.close()
        OCR.close()
        self.text=tk.StringVar()
        self.text.set(s)
        #按鈕標籤
        lb = tk.Label(self.Score,textvariable=self.text ,font=('microsoft yahei', '60','bold'),bg='#F1E5DC')
        img_sure='/home/pi/Desktop/Project/Picture/Rsure_Btn.png'
        btn_sure = btn_img(self.Score,300,150,img_sure,self.Back_ListenPage)
       
        #位置.
        lb.grid(row=0, padx=1400, pady=300, sticky="nw")
        btn_sure.grid(row=1, padx=1500, pady=150, sticky="nw")
        
    def Back_ListenPage(self,):#待設定回哪一個頁面       
        self.Score.destroy()
        ListenPage(self.master)
        
if __name__ == '__main__':    
    root = tk.Tk()
    basedesk(root)
    root.mainloop()