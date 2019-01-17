# import tensorflow as tf
# import keras
# import matplotlib.pyplot as plt
import nltk
import re
import sys
import numpy as np
# import csv
# from bs4 import BeautifulSoup
import pickle
import urllib.request
# import pandas as pd

def refine_abbr(text):
    text = re.sub(r"can\'t", "can not", text)
    text = re.sub(r"cannot", "can not", text)
    text = re.sub(r"what\'s", "what is", text)
    text = re.sub(r"What\'s", "what is", text)
    text = re.sub(r"that\'s", "what is", text)
    text = re.sub(r"That\'s", "what is", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"n\'t", " not", text)
    text = re.sub(r"i\'m", "i am", text)
    text = re.sub(r"I\'m", "i am", text)
    text = re.sub(r"you\'re", "you are", text)
    text = re.sub(r"I\'m", "i am", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"\'ll", " will", text)
    # text = re.sub(r" e mail ", " email ", text)
    # text = re.sub(r" e \- mail ", " email ", text)
    # text = re.sub(r" e\-mail ", " email ", text)
    return text


def remove_number(text):
    text = re.sub(r"0", "", text)
    text = re.sub(r"1", "", text)
    text = re.sub(r"2", "", text)
    text = re.sub(r"3", "", text)
    text = re.sub(r"4", "", text)
    text = re.sub(r"5", "", text)
    text = re.sub(r"6", "", text)
    text = re.sub(r"7", "", text)
    text = re.sub(r"8", "", text)
    text = re.sub(r"9", "", text)
    return text

with open('data_sentences_no_http_lower.pkl', 'rb') as f:
    data_sentences_no_http = pickle.load(f)
with open('data_sentences_videos_titles.pkl','rb') as f:
    data_sentences_videos_titles = pickle.load(f)

# print(data_sentences_raw[0])
titles=[]
for i,j,title in data_sentences_videos_titles:
# for i in range(len(data_sentences_no_http)):
#    for j in range(len(data_sentences_no_http[i])):
    if len(title)!=0:
        title=title[0]
        print(title)
        try:
            title = refine_abbr(title)
        except:
            print('wrong refine_abbr for %d, %d '%(i,j),title)
        try:
            title = remove_number(title)
        except:
            print('wrong remove_number for %d, %d'%(i,j),title)
        title = re.sub("[\.\!\/_,?:\[\]~$%@^#*\-(+\"\')]", "",title)
        for strr in title.split(' '):
            if strr!='':
                titles.append(strr.lower())
        print(titles)
        data_sentences_no_http[i][j]+=titles
        titles=[]

data_sentences_with_videos = data_sentences_no_http

# print(data_sentences_with_videos)

with open('data_sentences_with_videos.pkl','wb') as f:
  pickle.dump(data_sentences_with_videos, f, pickle.HIGHEST_PROTOCOL)

