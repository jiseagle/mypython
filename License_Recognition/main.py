# -*- coding: utf-8 -*-

import cv2
import numpy as np
from PIL import Image
import os.path
from skimage import data, io, filters

# 圖像拉伸函數
def img_stretch(img):
    maxi = float(img.max())
    mini = float(img.min())
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i, j] = (255/(maxi-mini)*img[i,j] - (255*mini)/(maxi-mini))
    
    return img

# 二值化處理
def binaryzation(img):
    maxi = float(img.max())
    mini = float(img.min())
    x = maxi - ((maxi-mini)/2)
    
    ret, threshimg = cv2.threshold(img, x, 255, cv2.THRESH_BINARY)
    
    return threshimg

# 尋找矩型輪廓
def find_rectangle(contours):
    y, x = [], []
    for p in contours:
        y.append(p[0][0])
        x.append(p[0][1])
    return [min(y), min(x), max(y), max(x)]

# 定位車牌
def locate_license(img1, orgimg):
    img, contours, hierarchy = cv2.findContours(img1, cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_SIMPLE)
        
    # 找出最大的三個區域
    block =  []
    for c in contours:    # 找出輪廓的左上點和右下點，並計算他的面積跟長度比
        r = find_rectangle(c)
        a = (r[2]-r[0])*(r[3]-r[1]) # 面積
        s = (r[2]-r[0])/(r[3]-r[1]) # 長度比
        block.append([r, a, s])
        
    # 選出前三個面積最大的區域
    block = sorted(block, key=lambda b: b[1])[-3:]
     
    # 使用顏色識別判斷找出最像車牌的區域
    maxweight, maxindex = 0, -1
    for i in range(len(block)):
        b = orgimg[block[i][0][1]:block[i][0][3],
                     block[i][0][0]:block[i][0][2]]
        
        #cv2.imshow('b Image', b)
    
        # BGR轉HSV
        hsvimg = cv2.cvtColor(b, cv2.COLOR_BGR2HSV)
        
        # 車牌顏色範圍
        lower = np.array([100, 50, 50])
        upper = np.array([140, 255, 255])
        
        # mask建構
        mask = cv2.inRange(hsvimg, lower, upper)
        
        # 統計權值
        w1 = 0
        for m in mask:
            w1 += m/255
        
        w2 = 0
        for w in w1:
            w2 +=w
        
        # 選出最大權值區域
        if w2 > maxweight:
            maxindex = i
            maxweight = w2
    
    return block[maxindex][0]
            
    
# 找車牌
def find_license(orgimg):
    # Resize圖片
    img = cv2.resize(orgimg, (400, int(400 * orgimg.shape[0]/orgimg.shape[1])))
    
    # 轉成灰階圖片
    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #hsvimg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 呼叫圖像拉伸副函數
    stretchimg = img_stretch(grayimg)
    
    # 定義元素結構 33x33 rectangular kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (33, 33))
    
    # 開運算 (Opening Operation)
    openingimg = cv2.morphologyEx(stretchimg, cv2.MORPH_OPEN, kernel)
    
    # 型態梯度
    #gradientimg = cv2.morphologyEx(stretchimg, cv2.MORPH_GRADIENT, kernel)
    
    # 計算Stretchimg 跟 openingimg的差分
    diffimg = cv2.absdiff(stretchimg, openingimg)
    
    # 對diffimg 做二值化
    binary_img = binaryzation(diffimg)
    
    # 使用Canny函數做Edge Detection
    cannyimg = cv2.Canny(binary_img, binary_img.shape[0], binary_img.shape[1])
    cv2.imshow('Canny Image', cannyimg)
    
    
    # 對Canny Img執行閉運算 (Closing Operation)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (19, 5))
    canny_closingimg = cv2.morphologyEx(cannyimg, cv2.MORPH_CLOSE, kernel)
    
    # 對closingimg執行開運算 (Opening Operation)
    closing_openingimg = cv2.morphologyEx(canny_closingimg, cv2.MORPH_OPEN, kernel)
    
    # 再次執行開運算
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,11))
    opening_closingimg = cv2.morphologyEx(closing_openingimg, cv2.MORPH_OPEN, kernel)
    
    rect = locate_license(opening_closingimg, img)
    
    return rect, img


# 讀取圖片
orgimg = cv2.imread('download.jpeg')
rect, img = find_license(orgimg)

# 框出車牌
cv2.rectangle(img, (rect[0], rect[1]), (rect[2], rect[3]), (0, 255,0), 2)

# 顯示圖片
cv2.imshow('Original Image', orgimg)
#cv2.imshow('Gray Image', grayimg)
cv2.imshow('Image', img)
#cv2.imshow('HSV Image', hsvimg)
#cv2.imshow('Stretch Image', stretchimg)
#cv2.imshow('Opening Image', openingimg)
#cv2.imshow('Closing Image', closingimg)
#cv2.imshow('Gradient Image', gradientimg)
#cv2.imshow('Diff Image', binary_img)
#cv2.imshow('Canny Image', cannyimg)
#cv2.imshow('Dilated Image', dilatedimg)

# 按下任意鍵則關閉所有視窗
cv2.waitKey(0)
cv2.destroyAllWindows()