import Conversion as cv
import re
import requests
import numpy as np
import pypinyin
from pypinyin import INITIALS, Style,pinyin,lazy_pinyin

def CheckTone(x):

    for c in range(5):
        if(x==cv.tones[c][0]):
            return(cv.tones[c][1])
def OCR_Transform(A,OCR_IN,OCR_FIN):

    for i in range (len(OCR_IN)):
        #轉換聲母的代碼
        for a in range (24):
            if(OCR_IN[i]==cv.initials[a][0]):
                A[i][1]=cv.initials[a][1]
                break
        #比對韻母的開頭字母，再去轉換代碼
        if (OCR_FIN[i].startswith('a')):
            a=re.split('(\D+)', OCR_FIN[i])
            for b in range(5):   
                if(a[1]==cv.finals[b][0]):
                    A[i][1]+=cv.finals[b][1]+CheckTone(a[2])
                    break
        elif (OCR_FIN[i].startswith('e')):
            a=re.split('(\D+)', OCR_FIN[i])
            for b in range(5,10):
                if(a[1]==cv.finals[b][0]):
                    A[i][1]+=cv.finals[b][1]+CheckTone(a[2])
                    break
        elif (OCR_FIN[i].startswith('i')):
            a=re.split('(\D+)', OCR_FIN[i])
            for b in range(10,20):
                if(a[1]==cv.finals[b][0]):
                    A[i][1]+=cv.finals[b][1]+CheckTone(a[2])
                    break
        elif (OCR_FIN[i].startswith('o')):
            a=re.split('(\D+)', OCR_FIN[i])
            for b in range(20,23):
                if(a[1]==cv.finals[b][0]):
                    A[i][1]+=cv.finals[b][1]+CheckTone(a[2])
                    break
        elif (OCR_FIN[i].startswith('u')):
            a=re.split('(\D+)', OCR_FIN[i])
            for b in range(23,32):
                if(a[1]==cv.finals[b][0]):
                    A[i][1]+=cv.finals[b][1]+CheckTone(a[2])
                    break
        else:
            for b in range(32,35):
                a=re.split('(\D+)', OCR_FIN[i])
                if(a[1]==cv.finals[b][0]):
                    A[i][1]+=cv.finals[b][1]+CheckTone(a[2])
                    break
def STT_Transform(B,STT_IN,STT_FIN):


  for i in range (len(STT_IN)):
    #轉換聲母的代碼
    for a in range (24):
      if(STT_IN[i]==cv.initials[a][0]):
        B[i]=cv.initials[a][1]
        break
    #比對韻母的開頭字母，再去轉換代碼
    if (STT_FIN[i].startswith('a')):
      a=re.split('(\D+)', STT_FIN[i])
      for b in range(5):   
        if(a[1]==cv.finals[b][0]):
          B[i]+=cv.finals[b][1]+CheckTone(a[2])
          break
    elif (STT_FIN[i].startswith('e')):
      a=re.split('(\D+)', STT_FIN[i])
      for b in range(5,10):
        if(a[1]==cv.finals[b][0]):
          B[i]+=cv.finals[b][1]+CheckTone(a[2])
          break
    elif (STT_FIN[i].startswith('i')):
      a=re.split('(\D+)', STT_FIN[i])
      for b in range(10,20):
        if(a[1]==cv.finals[b][0]):
          B[i]+=cv.finals[b][1]+CheckTone(a[2])
          break
    elif (STT_FIN[i].startswith('o')):
      a=re.split('(\D+)', STT_FIN[i])
      for b in range(20,23):
        if(a[1]==cv.finals[b][0]):
          B[i]+=cv.finals[b][1]+CheckTone(a[2])
          break
    elif (STT_FIN[i].startswith('u')):
      a=re.split('(\D+)', STT_FIN[i])
      for b in range(23,32):
        if(a[1]==cv.finals[b][0]):
          B[i]+=cv.finals[b][1]+CheckTone(a[2])
          break
    else:
      for b in range(32,35):
        a=re.split('(\D+)', STT_FIN[i])
        if(a[1]==cv.finals[b][0]):
          B[i]+=cv.finals[b][1]+CheckTone(a[2])
          break
def Order(A,B,score):
    
    for i in range(len(B)):
        check=False
        for j in range (len(A)):
            if(A[j][0]==1):#已配對完成
                continue
            elif(A[j][0]==0): #未配對
                print(B[i],A[j][1])
                if(B[i][:-1]==A[j][1][:-1]):  #若聲母和韻母皆一致
                    A[j][0]=1
                    score += 0.9
                    check=True
                    print(score,A[j][1])
                elif(B[i][:1]==A[j][1][:1]):#聲母配對得分
                    A[j][0]=1
                    score+=0.6
                    check=True
                    print(score,A[j][1])
                elif(B[i][1:2]==A[j][1][1:2]):  #韻母配對得分
                    A[j][0]=1
                    score+=0.3
                    check=True
                    print(score,A[j][1])
                if(A[j][0]==1 and B[i][-1]==A[j][1][-1]): #聲調配對得分
                    score += 0.1
                    check=True
                    print(score,A[j][1])
                if check:
                    break
                else:
                    continue
                             
    return score

def Order_Pro(A,B,score):

    indexA=0
    indexB=0
    for i in range(len(B)):
        check=False
        go=False
        for k in Initial: #檢查有無聲母
            if(B[i][0].find(k)==-1):
                go=False #無聲母
            else:
                go=True #有聲母
                break
        print(go)
        for j in range (len(A)):
            for k in Initial: #檢查有無聲母
                a=A[j][1][0].find(k)
                if(a!=-1):
                    break
            
            if(A[j][0]==1):#已配對完成
                continue
            elif(A[j][0]==0): #未配對
                print(B[i],A[j][1],j)
                if (go==True):
                    if(B[i][:-1]==A[j][1][:-1]):  #若聲母和韻母皆一致
                        A[j][0]=1
                        score+=0.9
                        check=True
                    elif(B[i][1:2]==A[j][1][1:2]):  #韻母配對得分
                        A[j][0]=1
                        score+=0.3+IniPro(A[j][1],B[i])*0.6
                        print(IniPro(A[j][1],B[i]),score)
                        check=True
                    else:
                      continue
                    '''elif(B[i][:1]==A[j][1][:1]):  #聲母配對得分
                        A[j][0]=1
                        score+=0.6
                        check=True
                   '''
                    
                elif(go==False and a==-1):
                    print(B[i])
                    if(B[i][:-1]==A[j][1][:-1]):  #若韻母皆一致
                        A[j][0]=1
                        score+=0.9
                        check=True
                    
                if(B[i][-1]==A[j][1][-1]): #聲調配對得分
                    score += 0.1
                    check=True
                    print(score,A[j][1])
                if check:
                    break
                else:
                    continue
                    
    return score

def IniPro(A,B):
    
    if(A[1]=='h'):
        indexA=A[0:2]
        
    else:
        indexA=A[0]
        
    if(B[1]=='h'):
        indexB=B[0:2]
        
    else:
        indexB=B[0]
    c=getValue(indexA,indexB)    
    print(indexA,indexB,c)
    return c
    
       
def getIndex(c):
    try:
        return index.index(c) #get index
    except:
        return -1

def getValue(a,b):
    index_a = getIndex(a) 
    index_b = getIndex(b)
    #  if index_a < 0 or index_b < 0:
    return values[index_a][index_b]

def DisplayScore(text1,text2): 
    while True:
        num =int(input())
        score=0
        if(num>0):
            #OCR聲母
            OCR_IN=np.array(lazy_pinyin(text1, style=Style.INITIALS, strict=False,errors='ignore'))
            length=len(OCR_IN)
            #print(OCR_IN)
            #OCR韻母+聲調
            OCR_FIN=np.array(lazy_pinyin(text1, style=Style.FINALS_TONE3, strict=False,errors='ignore'))
            #print(OCR_FIN)
            #STT聲母
            STT_IN=np.array(lazy_pinyin(text2, style=Style.INITIALS, strict=False,errors='ignore'))
            #print(STT_IN)
            #STT韻母+聲調
            STT_FIN=np.array(lazy_pinyin(text2, style=Style.FINALS_TONE3, strict=False,errors='ignore'))
            #print(STT_FIN)
            A=np.zeros([(len(OCR_IN)),2 ],dtype=object) #OCR轉換碼的陣列
            B=np.zeros([len(STT_IN),],dtype=object)  #STT轉換碼的陣列
            OCR_Transform(A,OCR_IN,OCR_FIN) 
            STT_Transform(B,STT_IN,STT_FIN)
            score+=Order(A,B,score)
            print(A)
            print(B)  


        elif (num==0):
            break

        else:
            OCRs=np.array(lazy_pinyin(text1, style=Style.TONE3, strict=False,errors='ignore'))
            STT=np.array(lazy_pinyin(text2, style=Style.TONE3, strict=False,errors='ignore'))
            OCR=np.zeros([(len(OCRs)),2 ],dtype=object)
            print(OCRs,STT)
            length=len(OCRs)
            
            for i in range(len(OCRs)):
                if (any(chr.isdigit() for chr in OCRs[i])==False):
                    OCRs[i]+="5"
                OCR[i][1]=OCRs[i]
                
            for i in range(0,len(STT)):
                if (any(chr.isdigit() for chr in STT[i])==False):
                    STT[i]+="5"
                
            score+=Order_Pro(OCR,STT,score)
           
        score=round((score/length)*100,2)
        print(str(score)+"%")
        
        
Initial=['b','p','m','f','d','t','n','l','g','k','h','j','q','x','zh','ch','sh','r','z','c','s','y','w']
#網路爬機率表格
url = 'https://yaru056.github.io/Pronunciation_Project/InitialTable.json'
data = requests.get(url).json()

index = data['index']
values = data['values']

score=0