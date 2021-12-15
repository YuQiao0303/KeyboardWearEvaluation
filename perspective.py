# coding: utf-8
import cv2
import numpy as np
from matplotlib import pyplot as plt
#全局变量
counter=0
down=False
width=474
height=465
corners=np.float32([[-1,-1],[-1,-1],[-1,-1],[-1,-1]])
canvas=np.float32([[0,0],[width,0],[0,height],[width,height]])

# mouse callback function
def find_corner(event,x,y,flags,param):
    global corners,counter,down
    if event == cv2.EVENT_LBUTTONDOWN: 
        down = True    #left button down
        #ix,iy = x,y
        #print "left button down"
    elif event == cv2.EVENT_LBUTTONUP:  #if release the left button
        if (down == True and counter<4):  #the final rectangle
            corners[counter] = [x,y]
            down=False
            print "得到坐标："
            print corners[counter]
            counter=counter+1
            
            
#透视变换函数
def pers(filename):
    global corners,counter,down,canvas,width,height
    counter=0
    down=False
    # create a window
    cv2.namedWindow('img')
    #注册回调函数
    cv2.setMouseCallback('img',find_corner)
    #读取文件并缩放
    img=cv2.imread(filename,0)
    zoom_width,zoom_height=612,816
    rows,cols=img.shape
    fx=float(zoom_width)/float(cols)
    fy=float(zoom_height)/float(rows)
    img=cv2.resize(img,None,fx=fx,fy=fy,interpolation=cv2.INTER_CUBIC)

    print "请按 左上，右上，左下，右下 的顺序，单击键盘区域的四角，之后按Esc"
    while(1):
        cv2.imshow('img',img)
        k=cv2.waitKey(1)
        if k== 27:
            break
    cv2.destroyAllWindows()
    
    #print corners
    #print "canvas:"
    #print canvas
    #透视变换
    M = cv2.getPerspectiveTransform(corners, canvas)
    result = cv2.warpPerspective(img, M, (0, 0))
    result=result[0:width,0:height]
    cv2.imshow('result',result)
    print "这是变换后的结果，看清楚后请按Esc"
    k=cv2.waitKey(0)
    if k== 27:
        cv2.destroyAllWindows()
    cv2.imwrite('pers_'+filename,result)
    return 
        
