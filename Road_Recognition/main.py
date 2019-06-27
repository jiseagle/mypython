# -*- coding:utf-8 -*-

import cv2
import matplotlib.pyplot as plt
import numpy as np


def get_edge(img):
    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurimg = cv2.GaussianBlur(grayimg, (13,13), 0)
    cannyimg = cv2.Canny(blurimg, 40, 120)
    return cannyimg

def get_roi(img):
    mask = np.zeros_like(img)
    points = np.array([[[146, 539], [781, 539], [515, 417],[296,397]]])
    cv2.fillPoly(mask, points, 255)
    roiimg = cv2.bitwise_and(edgeimg, mask)
    return roiimg

def get_avglines(lines):
    
    if lines is None:
        print("It cannot detect lines!!")
        return None
    
    lefts = []
    rights = []
    for line in lines:
        points = line.reshape(4,)
        x1, y1, x2, y2 = points
        slope, b = np.polyfit((x1, x2), (y1, y2), 1) # y = slope*x +b
                
        if slope > 0:
            rights.append([slope, b])
        else:
            lefts.append([slope, b])

    if rights and lefts:
        right_avg = np.average(rights, axis=0)
        left_avg = np.average(lefts, axis=0)
        return np.array([right_avg, left_avg])
    else:
        print("It cannot detect edges of left, and right")
        return None


def get_sublines(img, avglines):
    sublines =  []
    for line in avglines:
        slope, b = line
        y1 = img.shape[0]
        y2 = int(y1*(3/5))
        x1 = int((y1-b)/slope)
        x2 = int((y2-b)/slope)
        sublines.append([x1,y1,x2,y2])
    
    return np.array(sublines)

def draw_lines(img, lines):
    for line in lines:
        points = line.reshape(4,)
        x1, y1, x2, y2 = points
        cv2.line(img, (x1, y1), (x2, y2), (255,0,255), 3)
    return img

#img = cv2.imread("Frame_screenshot_26.06.2019.jpg")
#img = cv2.imread("road.jpg")
#sucess = 1
capture = cv2.VideoCapture("road.mp4")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (1280,720))

#out = cv2.VideoWriter('roadout.avi', cv2.VideoWriter_fourcc(*'DIVX'), 20, 
#           (640,480),True)

if capture.isOpened():
#if img is not None:
    while True:
        sucess, img = capture.read()
        if sucess:
            edgeimg = get_edge(img)
            roiimg = get_roi(edgeimg)
            lines = cv2.HoughLinesP(image=roiimg, rho = 3, theta = np.pi/180,
                        threshold=60, minLineLength=40,
                        maxLineGap=50)
            avglines = get_avglines(lines)
            
            if avglines is not None:
                sublines = get_sublines(img, avglines)
                img = draw_lines(img, sublines)
            else:
                print("It cannot detect lines")
            
            frame = img
            out.write(frame)
            cv2.imshow('Frame', img)
               
        key = cv2.waitKey(1)
        if key == ord('q'):
            print ("Exit")
            cv2.destroyAllWindows()
            capture.release()
            break
else:
    print("Error!!!!")

