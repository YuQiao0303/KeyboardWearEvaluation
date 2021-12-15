# coding: utf-8
import cv2
import numpy as np
from matplotlib import pyplot as plt

def getPos_ratio(pic_file_name,ratio,lrow,lcol,rrow,rcol):
      #读取图片
      sample1=cv2.imread(pic_file_name,0)
      #缩放
      width=474
      height=465
      rows,cols=sample1.shape
      fx=float(width)/float(cols)
      fy=float(height)/float(rows)
      sample1=cv2.resize(sample1,None,fx=fx,fy=fy,interpolation=cv2.INTER_CUBIC)
      #去噪
      sample1 = cv2.medianBlur(sample1,3)
      cut = cv2.medianBlur(sample1,3)
      cut1 = cv2.medianBlur(sample1,3)

      #---------------------切割，得到每一小块的左上角和右下角坐标---------------------
      lrow_list= []          #左上角row坐标
      lcol_list= []          #左上角col坐标
      rrow_list= []          #右下角row坐标
      rcol_list= []          #右下角col坐标

      rows,cols=cut.shape
      diff=3
      #对每一列
      lastsum=0
      for j in range(cols):
            sum=0
            #计算差分和sum
            for i in range(0,rows-1):
                  old=cut1[i,j]
                  new=cut1[i+1,j]
                  if old>new:
                        tem=old-new
                  else: tem=new-old
                  sum=sum+tem
                  
            #<1500的是无关像素，如果上一列是无关像素，当前列不是，当前列j是一个左上角的col坐标
            if (sum>=1500 and lastsum<1500):
                  lcol_list.append(j+diff+2)
          #<1500的是无关像素，如果上一列是有关像素，当前列不是，当前列j是一个右下角的col坐标
            if (sum<1500 and lastsum>=1500):
                  rcol_list.append(j-diff-5)
            lastsum=sum
      
      #对每一行
      lastsum=0
      #print cols,rows
      for i in range(rows):
            sum=0
            for j in range(0,cols-1):
                  old=cut1[i,j]
                  new=cut1[i,j+1]
                  if old>new:
                        tem=old-new
                  else: tem=new-old
                  sum=sum+tem
          #<1500的是无关像素，如果上一行是无关像素，当前行不是，当前行i是一个左上角的row坐标
            if (sum>=1500 and lastsum<1500):
                  lrow_list.append(i+diff)
          #<1500的是无关像素，如果上一行是有关像素，当前行不是，当前行i是一个左上角的row坐标
            if (sum<1500 and lastsum>=1500):
                  rrow_list.append(i-diff)
            lastsum=sum

      
              
      #自适应门限
      binary = cv2.adaptiveThreshold(sample1,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                      cv2.THRESH_BINARY,11,13)
      #binary = cv2.adaptiveThreshold(cut,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
      #            cv2.THRESH_BINARY,11,2)
      #_,binary = cv2.threshold(cut,50,255,cv2.THRESH_BINARY)

      #计算每一按键小块中，黑色像素占的比例ratio,得到每一个小块的图像roi
      block=[]
      counter=0

      for i in range(0,4):
          for j in range(0,4):
              block.append(binary[lrow_list[i]:rrow_list[i],lcol_list[j]:rcol_list[j]])
              #计算黑色像素个数
              total=0
              black=0
              for x in range(lrow_list[i],rrow_list[i]):
                  for y in range(lcol_list[j],rcol_list[j]):
                      total=total+1
                      if binary[x,y]==0:
                          black=black+1
              ratio[counter]=(float(black)/float(total))
              #print i,j,black,total,ratio[counter]
              counter=counter+1
              #print " "
    
      for i in range(0,4):
            lrow[i]=lrow_list[i]
            lcol[i]=lcol_list[i]
            rrow[i]=rrow_list[i]
            rcol[i]=rcol_list[i]
      print "lrow",lrow
      print "rrow",rrow
      print "lcol",lcol
      print "rcol",rcol
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

      return 

