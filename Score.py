import numpy as np
import pypinyin
from pypinyin import INITIALS, Style,pinyin,lazy_pinyin

import requests

global score
score=0
tones=[

  ["","L"],
  ["1","M"],
  ["2","N"],
  ["3","O"],
  ["4","P"]
]
#網路爬機率表格
url = 'https://yaru056.github.io/Pronunciation_Project/InitialTable.json'
url1 = 'https://yaru056.github.io/Pronunciation_Project/FinalTable.json'
In_data = requests.get(url).json()
Fin_data = requests.get(url1).json()

In_index = In_data['index']
In_values = In_data['values']

Fin_index = Fin_data['index']
Fin_values = Fin_data['values']

class Temp:
  def __init__(self, sound):
    self.sound = sound
    self.ocr = {} #key:ocr的index(和stt比) value:index差
    self.stt = []

  #push 拼音和OCR相同的index
  def push_ocr(self, key, item):
    if not key in self.ocr.keys():
      self.ocr[key] = []
    self.ocr[key].append(item)
  #push 拼音和STT相同的index，就可以記錄在同一個ocr
  def push_stt(self, item):
    self.stt.append(item)
  #組合Output
  def __str__(self):
    return self.sound + ': ' + str(self.stt) + ' ' + str(self.ocr)
  def push_index(self,item):
    self._index.append(item)

def Find(arr, item): #尋找陣列中相同的元素值，紀錄index
  i =  0
  _arr = []
  while i < len(arr):
    if (arr[i] == item):
      _arr.append(i)
    i += 1
  return _arr

def Tone(x,y):
  if(x==y):
    global score
    score+=0.1
    #print("Yes")

def CheckTone(x): #把聲調換掉
    x=x[-1]
    for c in range(5):
        if(x==tones[c][0]):
            return(tones[c][1])
def Ini(A): #找出聲母是誰
  if(A[1:2]=='h'):
    return(A[0:2])
  else:
    return(A[0:1])

def Fin(A): #找出聲母是誰
  if(A[1:2]=='h'):
    return(A[2:])
  else:
    return(A[1:])

def check_duplicates(list1): #找出list中相同index差的index並放入index_same裡面
  index_same=[]
  for e in set(list1):
    if list1.count(e) > 1:
      index_same.append(e)
  return index_same

def get_key(dict,value): #用value找key
  return [k for k,v in dict.items() if v==value]

def one_to_one(index,key):
  STT_Order[index]=key[0]
  global score
  score+=0.9
  
def one_to_many(index,key):
  STT_Order[index]=key
  global score
  score+=0.9
  
def many_to_one(index,key):
  STT_Order[index]=key[0]
  global score
  score+=0.9
  
def many_to_many(index,key):
  STT_Order[index]=key
  global score
  score+=0.9

#找機率的function
def IniPro(A,B):
    
    if(A[1]=='h'):
        indexA=A[0:2]
        
    else:
        indexA=A[0]
   
    if(B[1]=='h'):
        indexB=B[0:2] 
    else:
        indexB=B[0]

    
    c=getValue(indexA,indexB,"In")    
    print(indexA,indexB,c)
    return c

def FinProPre(In,A):
  if(A=="ve"):
    A="ue"

  if(In=="j" or In=="q" or In=="x"):
    if(A=="u"):
      A="v"
    elif(A=="uan"):
      A="uan1"
    elif(A=="un"):
      A="un1"
  elif(In=="y"):
    if(A=="a"):
      #print("取MAX(ai,a)")
      A="ai"
    elif(A=="o"):
      A="io"
    elif(A=="e"):
      A="ei"
    elif(A=="u"):
      A="v"
    elif(A=="uan"):
      A="uan1"
    elif(A=="un"):
      A="un1"
  
  return A


def FinPro(A,B):
    
    if(A[1]=='h'):
        indexA=A[2:]
        
    else:
        In=A[0:1]
        indexA=A[1:]
        indexA=FinProPre(In,indexA)

    if(B[1]=='h'):
        indexB=B[2:]
    
    else:
        In=B[0:1]
        indexB=B[1:]
        indexB=FinProPre(In,indexB)

    
    c=getValue(indexA,indexB,"Fin")    
    print(indexA,indexB,c)
    return c    
       
def getIndex(c,d):
    try:
      if(d=='In'):
        return In_index.index(c) #get index
      elif(d=='Fin'):

        return Fin_index.index(c) #get index
    except:
        return -1

def getValue(a,b,c):
    index_a = getIndex(a,c) 
    index_b = getIndex(b,c)
    #  if index_a < 0 or index_b < 0:
    if(c=='In'):
      return In_values[index_a][index_b]
    elif(c=='Fin'):
      return Fin_values[index_a][index_b]

#Initial=['b','p','m','f','d','t','n','l','g','k','h','j','q','x','zh','ch','sh','r','z','c','s','y','w']



def Display_Score(text1,text2):
  OCR_tone=np.array(lazy_pinyin(text1, style=Style.TONE3, strict=False,errors='ignore'))
  print(OCR_tone)

  STT_tone=np.array(lazy_pinyin(text2, style=Style.TONE3, strict=False,errors='ignore'))
  print(STT_tone)

  ocr=lazy_pinyin(text1, style=Style.NORMAL, strict=False,errors='ignore')
  print(ocr)
  stt=lazy_pinyin(text2, style=Style.NORMAL, strict=False,errors='ignore')
  print(stt)

  global STT_Order,score
  score=0
  STT_Order=np.full((len(stt)),-1)

  result = []
  stt_clone = [i for i in stt]

  while len(stt_clone):
    obj = Temp(stt_clone[0])
    #obj.push_stt(k)
    
    position = Find(stt,stt_clone[0])#把stt此元素和stt list相比 相同的紀錄起來
    for i in position:
      #print('stt',i)
      obj.push_stt(i)
      #print(obj.stt)
    position = Find(ocr,stt_clone[0])#把stt此元素和ocr list相比 相同的紀錄起來
    for i in position:
      #計算差值並放入物件中_index的陣列
      for j in obj.stt:
        index=abs(i-j)
        obj.push_ocr(i, index)
        #print(obj.ocr)

    stt_clone = list(filter(lambda a: a != stt_clone[0], stt_clone))
    #result裡面有很多個不同發音的temp物件
    result.append(obj)



  check_none=False #檢查是否有(無相同的聲母韻母)
  none=[] #記錄無相同聲母、韻母的STTindex

  for i in range(len(OCR_tone)):
    OCR_tone[i]=CheckTone(OCR_tone[i])
  for i in range(len(STT_tone)):
    STT_tone[i]=CheckTone(STT_tone[i])  

  print(OCR_tone,STT_tone)

  #比對順序及查詢機率表
  #處理A部分(紀錄相同聲母和韻母)
  for i in range (len(result)):
    print(result[i])
    stt_len=len(result[i].stt)
    ocr_key_len=len(result[i].ocr)
    index=result[i].stt[0]
    if(stt_len==0):
      continue
    elif(stt_len==1):
      
      if(ocr_key_len==0):
        print("無相同的聲母和韻母")
        check_none=True
        none.append(index)
        print(none)
      elif(ocr_key_len==1):
        print("1對1")
        key=list(result[i].ocr.keys())#This is a list
        one_to_one(index,key)
        Tone(STT_tone[index],OCR_tone[key[0]])
      else:
        print("1對多")
        #把字典列表化取得key值
        key=list(result[i].ocr.keys())[list(result[i].ocr.values()).index(min(list(result[i].ocr.values())))] #This is a int
        one_to_many(index,key)
        Tone(STT_tone[index],OCR_tone[key])
        
    else:
      if(ocr_key_len==0):
        print("無相同的聲母和韻母")
        check_none=True
        none.append(index)
        print(none)
      elif(ocr_key_len==1):
        print("多對1")
        a=list(result[i].ocr.values())
        index=result[i].stt[a[0].index(min(a[0]))]
        key=list(result[i].ocr.keys()) #This is a list
        many_to_one(index,key)
        Tone(STT_tone[index],OCR_tone[key[0]])
        
      else:
        print("多對多")
        #檢查是否有相同的index差
        same=[]  #紀錄index的差之最小值有相同的index差
        del_index=[]
        min_index=[-1]*len(stt) #紀錄在stt相同位置下最小的index差
        min_key=[-1]*len(stt) #紀錄在stt相同位置下最小的index差 下配對的key(OCR的index)
        No_same=False 
        while (len(result[i].ocr)!=0 and len(result[i].stt)!=0 ):
          
          
          del_index=[]
          min_index=[-1]*len(stt) #紀錄在stt相同位置下最小的index差
          min_key=[-1]*len(stt) #紀錄在stt相同位置下最小的index差 下配對的key(OCR的index)
          for val in list(result[i].ocr.values()):
            check_same=check_duplicates(val)
            val_min=min(val)
            
            
            if(val_min not in check_same): #若min(index差)不再重複值裡面
              No_same=True
              print(val_min)
              print(result[i].stt)
              print("index的差之最小值無相同的index差")
              index=result[i].stt[val.index(val_min)]
              key=list(result[i].ocr.keys())[list(result[i].ocr.values()).index(val)]
              
              
              if(min_index[index]==-1):
                min_index[index]=val_min
                min_key[index]=key
              elif(min_index[index]>val_min):
                min_index[index]=val_min
                min_key[index]=key
                print("min Key")
                print(min_key)

            else:
              print("index的差之最小值有相同的index差")
              index=result[i].stt[val.index(val_min)]
              key=list(result[i].ocr.keys())[list(result[i].ocr.values()).index(val)]
              print(index,key)
              many_to_many(index,key)
              Tone(STT_tone[index],OCR_tone[key])
              del result[i].ocr[key]
          print(result[i].ocr)
          if No_same:
            for k in min_key:
              if(k!=-1):
                index=min_key.index(k)
                key=k
                print(index,key)
                many_to_many(index,key)
                Tone(STT_tone[index],OCR_tone[key])
                del_index.append(result[i].stt.index(index))
                del result[i].ocr[key] #把已配對好的ocr的index刪掉
                
              else:
                continue
         
          
          del_index.sort(reverse=True)
          #print(del_index)
          for j in del_index:
            #print ("result:"+str(i)+" del_index:"+str(j))
            del result[i].stt[j]
            for m in list(result[i].ocr.keys()):
              print(m)
              del result[i].ocr[m][j]
              print(list(result[i].ocr[m]))
          print (result[i].ocr)
          del_index=[] 
          

            
    #print(STT_Order,none)

  #處理B部分(紀錄相同聲母))
  ocr_set=set()
  for i in range(len(ocr)):
    ocr_set.add(i)
  if check_none:
    _set=set(STT_Order) #把已配對的OCR index做排序
    _set.discard(-1) #集合內放入所有以配對好的OCR index，把-1拿掉
    a=ocr_set.difference(_set) #未配對的OCR index:把ocr_set和已經和stt配對的index取差集
    print(a,none)
    #print(STT_Order)
    none_in=[]
    for i in none:
      
      proscore=[0,0]
      
      for j in a:
        #print(j)
        #print("STT:"+Ini(stt[i]))
        #print("OCR:"+Ini(ocr[j]))
        if(Ini(stt[i])==Ini(ocr[j])):
          print(stt[i],ocr[j])
          c=FinPro(stt[i],ocr[j])
          if(c>proscore[0]):
            proscore[0]=c
            proscore[1]=j
        else:
          #print("NO")
          continue
      if(proscore[0]!=0):
        STT_Order[i]=proscore[1]
        a.discard(proscore[1])
        #print(proscore[1])
        #none.remove(i)
        none_in.append(i)
        
        score+=0.6
        score+=0.3*proscore[0]
        Tone(STT_tone[i],OCR_tone[j])
        #print(score,none)
    for i in none_in:
      none.remove(i)
  #處理C部分
  if(len(none)!=0):

    for i in none:
      proscore=[0,0]
      
      for j in a:
        #print(j)
        if(Fin(stt[i])==Fin(ocr[j])):
          #print(stt[i],ocr[j])
          c=IniPro(stt[i],ocr[j])
          if(c>proscore[0]):
            proscore[0]=c
            proscore[1]=j
        else:
          #print("NO")
          continue
      if(proscore[0]!=0):
        #print(none)
        STT_Order[i]=proscore[1]
        #print(proscore[1])
        a.discard(proscore[1])
        none.remove(i)
        score+=0.3
        score+=0.6*proscore[0]
        Tone(STT_tone[i],OCR_tone[j])
  print(STT_Order,none,score)
  STT_Order=list(STT_Order)
  #處理順序問題
  while(-1 in STT_Order):
    STT_Order.remove(-1)
  if(STT_Order == sorted(STT_Order)):
    print("Yes")
  else:
    print(STT_Order,sorted(STT_Order))
    score*=0.95
  return (str(round(score/len(ocr),3)*100))


