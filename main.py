# -*- coding: UTF-8 -*-
import getPos_ratio      #导入能得到16个按键位置且算出每块黑色像素比的函数
import cal_ratio         #导入能根据给定位置算出每块黑色像素比的函数
import perspective       #导入能将键盘区域变成标准矩形

#--------------对四副样本图进行透视投影，将键盘区域变成标准矩形--------------------------
file_name=['1.jpg','2.jpg','3.jpg','4.jpg']
for i in range(0,4):
    perspective.pers(file_name[i])
    
for i in range(0,4):
      file_name[i]="pers_"+file_name[i]

#-----------------------处理样本，得到样本的黑色像素比ratio-------------------------------
ratio,abbrasion,lrow,lcol,rrow,rcol=[],[],[],[],[],[]
for i in range(0,4):
      lrow.append(0.0)
      lcol.append(0.0)
      rrow.append(0.0)
      rcol.append(0.0)
      ratio=ratio+[[]]
      abbrasion=abbrasion+[[]]
      for j in range(0,16):
            ratio[i]=ratio[i]+[0.0]
            abbrasion[i]=abbrasion[i]+[0.0]

         #先用一个样本得到位置和ratio   
getPos_ratio.getPos_ratio(file_name[3],ratio[3],lrow,lcol,rrow,rcol)
            #再利用刚才求出的位置，求其他样本的ratio
for i in range(0,3):
      cal_ratio.cal_ratio(file_name[i],ratio[i],lrow,lcol,rrow,rcol)

  
#----------------------------处理模板，得到模板的ratio------------------------
model_name="model.jpg"
ratio_model=[]
for i in range(0,16):
    ratio_model.append(0.0)
cal_ratio.cal_ratio(model_name,ratio_model,lrow,lcol,rrow,rcol)

#---------------------------------磨损度-----------------------------

for i in range(0,4):
    for j in range(0,16):
        res=1-(ratio[i][j]/ratio_model[j])
        abbrasion[i][j]=res
        #print abbrasion[i][j]
    #print "第",i+1,"幅图16键磨损度："
    #for k in range(0,4):
        #print ("%.3f   %.3f   %.3f   %.3f"%(abbrasion[i][k],abbrasion[i][k+1],abbrasion[i][k+2],abbrasion[i][k+3]))

#求平均值
ave=[]
for j in range(0,16):
      final=0
      for i in range(0,4):
            final+=abbrasion[i][j]
      final/=4
      ave.append(final)
      
print "四幅图中，十六个键的平均磨损程度为："
for i in range(0,4):
      print ("%.3f   %.3f   %.3f   %.3f"%(ave[i],ave[i+1],ave[i+2],ave[i+3]))
      
      
      
