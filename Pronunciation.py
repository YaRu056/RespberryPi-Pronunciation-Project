import os
import re
import sys
import tkinter as tk
import OCR_Read as ocr
import txtSpeak as sp
import SpeechRecog as spr
import Comparison as com

      
file1 = '/home/pi/Desktop/Project/OCR_Output.txt'
file2 = '/home/pi/Desktop/Project/STT.txt'

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
        
        btn_scan = tk.Button(self.Mainpage,text='掃描',font=('標楷體', '40'),command=self.Go_CameraPage)
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
        
class instructions_page():
    def __init__(self,master):
        self.master = master
        self.master.config(bg='gray')
        self.instructions_page = tk.Frame(self.master,)
        self.instructions_page.pack()
        '''
        img= ImageTk.PhotoImage(Image.open('test.jpg'))
        label_right= tk.Label(self.instructions_page,height=700,width=480,bg ='gray94',fg='blue',image = img) 
        label_right.grid(row=1,column=0,padx=20, pady=20, sticky="nw") '''
        
        btn_sure = tk.Button(self.instructions_page,text='確定',font=('標楷體', '40'),command=self.Back_mainpage)
        btn_sure.pack()
        
    def Back_mainpage(self,):       
        self.instructions_page.destroy()
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
    
    def leave(self):
        self.CameraPage.destroy()
        Mainpage(self.master)
        
    def photo_again(self):
        #開始拍照 圖片轉文字
        ocr.Camera()
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
ocr.Camera()
    

#念出圖像中的文字
OCR=open(file1,'r',encoding="utf-8")
text1=OCR.read()

if(text1==""):
    print("No text!")    
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

OCR.close()
STT.close()

