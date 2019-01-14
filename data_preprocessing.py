#import tensorflow as tf
# import keras
import matplotlib.pyplot as plt
import nltk
import re
import sys
import numpy as np
import csv
from bs4 import BeautifulSoup
import pickle
import urllib.request

import pandas as pd

def grab(url):
    # 打开传入的网址
    resp = urllib.request.urlopen(url)
    # 读取网页源码内容
    data = resp .read()
    return data

def grab2(url):
    with open(url, 'r', encoding='gbk') as f:
        Soup = BeautifulSoup(f.read(), 'lxml')
        titles = Soup.select('body > div.main-content > ul > li > div.article-info > h3 > a')  # 标题
    return titles




# raw_data = pd.read_csv('mbti_1.csv')
#
# label = raw_data['type'].tolist()
# # print(label)
#
# data_sentence = raw_data['posts'].tolist()
#
# data_sentences = []
# for items in data_sentence:
#     item = [x for x in items.split('|||')]
#     data_sentences.append(item)
# # print(len(data_sentences),len(data_sentences[0]))
#
# data_videos = []
# data_jpgs = []
# for i in range(len(data_sentences)):
#     item = data_sentences[i]
#     for j in range(len(item)):
#         if 'http' in item[j] and '.jpg' not in item[j]:
#             data_videos.append((i,j,item[j]))
#         if 'http' in item[j] and '.jpg' in item[j]:
#             data_jpgs.append((i,j,item[j]))
#
# print('a',len(data_videos))
# print('b',len(data_jpgs))
#
# with open('label.pkl', 'wb') as f:
#   pickle.dump(label, f, pickle.HIGHEST_PROTOCOL)
# with open('data_sentences.pkl','wb') as f:
#   pickle.dump(data_sentences, f, pickle.HIGHEST_PROTOCOL)
# with open('data_videos.pkl','wb') as f:
#   pickle.dump(data_videos, f, pickle.HIGHEST_PROTOCOL)
# with open('data_jpgs.pkl','wb') as f:
#   pickle.dump(data_jpgs, f, pickle.HIGHEST_PROTOCOL)

with open('data_videos.pkl', 'rb') as f:
    data_videos = pickle.load(f)

data_videos_title = []
for m in range(len(data_videos)):
    i,j,url = data_videos[m]
    titles = str(grab(url))
    title = re.findall(r"\"title\"\:\"(.*?)\"",titles)
    print(title)
    data_videos_title.append((i,j,title))

with open('data_videos_title.pkl','wb') as f:
    pickle.dump(data_videos_title, f, pickle.HIGHEST_PROTOCOL)

print('data_videos_title generate finish')
sys.stdout.flush()






