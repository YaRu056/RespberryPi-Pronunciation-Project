import cv2
#import read

def image_func():

    #img = cv2.imread('./pic/1.png', 0)	
    img = cv2.imread('/home/pi/Desktop/Project/Picture/OCRImage.jpg', 0)	# 以灰度模式開啟圖片生成圖片物件

    # 先列出用到的預處理手段：

    # 虛化處理
    blurMedian = cv2.medianBlur(img, 3)	# 中值虛化處理p2
    blurGaussian = cv2.GaussianBlur(img,(5,5),0)	# 高斯虛化處理p1

    # 闕值處理

    # 最直接的闕值處理 p3
    simpleThreshold = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]
    # 規定一個闕值127，小於的是背景，大於的是文字(255)。cv2.THRESH_BINARY位置還有其他引數可控選擇，參見opencv-python的技術文件。返回一個列表，列表有兩個元素，第二個元素是處理的圖片物件，所以索引用1

    # 中值自適應闕值處理p4
    adaptiveThreshold1 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    # cv2.ADAPTIVE_THRESH_MEAN_C，闕值取鄰近區域的中值。返回處理後的圖片物件，注意第一個引數影象物件img必須是灰度模式

    # 高斯自適應闕值處理p5
    adaptiveThreshold2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # cv2.ADAPTIVE_THRESH_GAUSSIAN_C闕值是加了權重的鄰近區域值的和，而這個權重的計算使用了高斯窗（Gaussian Window）

    # OTSU二值化處理p6
    otsuThreshold1 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU) [1]

    # 先高斯虛化過濾後，再做OTSU二值化處理 p7
    otsuThreshold2 = cv2.threshold(blurMedian, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    # 也可以先中值虛化後跟自適應闕值處理組合，先高s斯虛化後過濾後再自適應闕值處理，看哪個預處理預處理效果好。接下來把處理手法名稱字串加入列表，作為視窗顯示的標題。

    titles = ['Original Image0', 'Gaussian filtered Image1', 'Median blur2', 'Global Thresholding(v=127)3', 'Adaptive Mean Thresholding4', 'Adaptive Gaussian Thresholding5', "Otsu's Thresholding6", "Otsu's Thresholding after Gaussian filter7"]
    # 預處理後顯示視窗的視窗標題列表
    #cv2.namedWindow('GreyModeOpen',cv2.WINDOW_NORMAL)
    images = [img, blurGaussian, blurMedian, simpleThreshold, adaptiveThreshold1, adaptiveThreshold2,otsuThreshold1, otsuThreshold2]
    # 預處理後的圖片物件




    for i in range(len(images)):
        #cv2.namedWindow(titles[i],cv2.WINDOE_NORMAL)
        cv2.imshow(titles[i], images[i])
        path = ('/home/pi/Desktop/Project/img_text/p')
         #顯示預處理後的圖片，視窗標題從標題列表中取，預處理 後的圖片物件從物件列表中取
        cv2.imwrite(path+str(i)+'.jpg',images[i])
        cv2.waitKey(0)
        
        # 等待敲擊鍵盤結束本次迴圈，開始下一次迴圈。注意對敲鍵盤有反應必須在圖片視窗是前端的情況下（前段視窗標題背景為藍，後段視窗標題背景為灰色）

    #read.read_func()

        
