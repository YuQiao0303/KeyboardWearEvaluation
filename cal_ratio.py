# coding: utf-8
import cv2
import numpy as np
from matplotlib import pyplot as plt
def cal_ratio(pic_file_name,ratio,lrow,lcol,rrow,rcol):
    #读取图片
    sample1=cv2.imread(pic_file_name,0)
    #sample1=cv2.imread('new.png',0)
    #缩放
    width=474
    height=465
    rows,cols=sample1.shape
    rows,cols=sample1.shape
    fx=float(width)/float(cols)
    fy=float(height)/float(rows)
    sample1=cv2.resize(sample1,None,fx=fx,fy=fy,interpolation=cv2.INTER_CUBIC)

    #去噪
    sample1 = cv2.medianBlur(sample1,3)
    #sample1 = cv2.blur(sample1,(3,3))
    #down=cv2.blur(down,(5,5))
    cut = cv2.medianBlur(sample1,3)
    cut1 = cv2.medianBlur(sample1,3)

    #自适应门限
    binary = cv2.adaptiveThreshold(sample1,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                    cv2.THRESH_BINARY,11,13)
    #binary = cv2.adaptiveThreshold(cut,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
    #            cv2.THRESH_BINARY,11,2)
    #_,binary = cv2.threshold(cut,50,255,cv2.THRESH_BINARY)

    #计算每一按键小块中，黑色像素占的比例ratio,得到每一个小块的图像roi
    block=[]
    counter=0
    diff=3
    for i in range(0,4):
        for j in range(0,4):
            if(pic_file_name=='model.jpg'):
                block.append(binary[lrow[i]+diff:rrow[i],lcol[j]:rcol[j]-diff])
                #计算黑色像素个数
                total=0
                black=0
                for x in range(lrow[i]+diff,rrow[i]):
                    for y in range(lcol[j],rcol[j]-diff):
                        total=total+1
                        if binary[x,y]==0:
                            black=black+1
                ratio[counter]=(float(black)/float(total))
                #print i,j,black,total,ratio[counter]
                counter=counter+1
            if(pic_file_name!='model.jpg'):
                block.append(binary[lrow[i]:rrow[i],lcol[j]:rcol[j]])
                #计算黑色像素个数
                total=0
                black=0
                for x in range(lrow[i],rrow[i]):
                    for y in range(lcol[j],rcol[j]):
                        total=total+1
                        if binary[x,y]==0:
                            black=black+1
                ratio[counter]=(float(black)/float(total))
                #print i,j,black,total,ratio[counter]
                counter=counter+1



    #显示
    print "此图为",pic_file_name,"处理后的结果，看清楚后直接点×关闭即可"
    titles = []
    for i in range(0,16):
        titles.append(i)
          

    for i in xrange(16):
        plt.subplot(4,4,i+1),plt.imshow(block[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
    plt.show()

    return ratio

          
      
    
