
import time
import os
import string
from gtts import gTTS
from pygame import mixer
import tempfile

def speak(sentence, lang):
    #with tempfile.NamedTemporaryFile(delete=True) as fp:
    tts=gTTS(text=sentence, lang=lang)
    tts.save("/home/pi/Desktop/Project/OCRtext.mp3")
    mixer.init()
    mixer.music.load("/home/pi/Desktop/Project/OCRtext.mp3")
    mixer.music.play(1)
    
def speak1():
    #with tempfile.NamedTemporaryFile(delete=True) as fp:
    
    mixer.init()
    mixer.music.load("/home/pi/Desktop/Project/in.mp3")
    mixer.music.play(1)
    
def countWords(s): 
    words = str.split(s) 
    return len(words)

def speak_all():
    
   
      
    total_words = 0;   
       
    
    path = '/home/pi/Desktop/Project/OCR_Output.txt'
    f = open(path, 'r',encoding='utf-8')
    line = f.read()
    #print(line)
    total_words = 0;
    
    
    
    speak(line, 'zh-tw')
    for word in line:
        total_words = total_words + countWords(word)
    print(total_words)
    time.sleep((total_words/3)+1)
    
    f.close()
    mixer.music.load("/home/pi/Desktop/Project/OCRtext_copy.mp3")
    os.remove("/home/pi/Desktop/Project/OCRtext.mp3")

def test():
    mixer.init()
    print("OH")
    mixer.music.load("/home/pi/Desktop/Project/OCRtext_copy.mp3")
    mixer.music.play(1)

