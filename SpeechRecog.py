fromLanguage = "zh-TW"
toLanguage = "en"

import time
import os
from os import path
import speech_recognition as sr
from textblob import TextBlob
from gtts import gTTS  #利用google gTTS將文字轉成語音

#tts = gTTS(text="您好,我是語音辨識助理", lang=fromLanguage)
#tts.save("tts.mp3")
#os.system('omxplayer -p -o local tts.mp3')
#time.sleep(0.5)

def speech_recognition():

    check=True
    while check:


      try:
        #使用麥克風為信號源
        r = sr.Recognizer()
        mic=sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source)
            print("Say something!")
            #使用麥克風獲取參數，檢測到靜止後會停止
            audio = r.listen(source)
        print("Record end")
        
        #語音轉文字
        sttTXT_org= r.recognize_google(audio, language=fromLanguage)
        print("Google Speech Recognition thinks you said --> " + sttTXT_org)
        #if sttTXT_org==-1:
            #continue

        #寫入檔案
        path = '/home/pi/Desktop/Project/STT.txt'#暫定檔名
        f = open(path,'w')
        f.write(sttTXT_org)
        f.close()
        check=False
        
        #念出識別結果
        #tts = gTTS(text="您剛剛說的語句是." +sttTXT_org, lang=fromLanguage)
        #tts.save("tts.mp3")
        #os.system('omxplayer -p -o local tts.mp3')
        #time.sleep(0.5)

      #處理例外狀況
      except sr.UnknownValueError:
           print("Google Speech Recognition could not understand audio")
           tts = gTTS(text="您剛剛說的我沒聽懂,麻煩您再說一次", lang=fromLanguage)
           tts.save("tts.mp3")
           os.system('omxplayer -p -o local tts.mp3')
           time.sleep(0.5)

      except sr.RequestError as e:
           print("Could not request results from Google Speech Recognition service; {0}".format(e))
           time.sleep(0.5)
