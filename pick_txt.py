# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 14:24:33 2019

@author: dell-
"""

import pickle
import codecs
import re
Raw_Pkl_File='data/data_sentences_no_http.pkl'
Lable_Pkl_File='data/label.pkl'
Lable_Txt_File='data/label.txt'
Train_Pkl_File='data/Train.pkl'
Test_Pkl_File='data/Test.pkl'
Raw_Txt_File='data/data_sentences_no_http.txt'
Train_Txt_File='data/Train.txt'
Test_Txt_File='data/Test.txt'
Train_Txt_withlabel__File='data/train_with_label.txt'
Test_Txt_withlabel__File='data/test_with_label.txt'
raw_text=pickle.load(open(Raw_Pkl_File,'rb'),encoding='utf-8')
raw_label=pickle.load(open(Lable_Pkl_File,'rb'),encoding='utf-8')
print(len(raw_text))
print(len(raw_text[0]))
###cut pkl file
train_set=raw_text[1000:len(raw_text)]
test_set=raw_text[0:1000]
with open(Train_Pkl_File, 'wb') as f:
    pickle.dump(train_set, f, pickle.HIGHEST_PROTOCOL)
with open(Test_Pkl_File, 'wb') as f:
    pickle.dump(test_set, f, pickle.HIGHEST_PROTOCOL)
##convet pkl to txt
file1=open(Raw_Txt_File,'w',encoding='utf-8')
file2=open(Train_Txt_withlabel__File,'w',encoding='utf-8')
file3=open(Test_Txt_withlabel__File,'w',encoding='utf-8')
file4=open(Train_Txt_File,'w',encoding='utf-8')
file5=open(Test_Txt_File,'w',encoding='utf-8')
for i in range(1000):###training set
    Str=""
    for j in range(len(raw_text[i])):
        s=str(raw_text[i][j]).replace('[',"").replace(']',"")
        s=s.replace("'","").replace(",","").replace("=","").replace(";","")
        Str = Str + s
    file1.write(Str+'\n')
    file3.write(Str+"\t"+"__label__"+str(raw_label[i])+'\n')
    file5.write(Str + '\n')
file5.close()
file3.close()
for i in range(1000,len(raw_text)):###training set
    Str=""
    for j in range(len(raw_text[i])):
        s=str(raw_text[i][j]).replace('[',"").replace(']',"")
        s=s.replace("'","").replace(",","").replace("=","").replace(";","")
        Str =Str+s
    file1.write(Str+'\n')
    file4.write(Str + '\n')
    file2.write(Str+"\t"+"__label__"+str(raw_label[i])+'\n')
file2.close()
file4.close()
file1.close()
file6=open(Lable_Txt_File,'w',encoding='utf-8')
for lab in raw_label:
    file6.write(str(lab)+'\n')
file6.close()
