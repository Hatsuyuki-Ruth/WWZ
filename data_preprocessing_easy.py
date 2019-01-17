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
import pandas as pd


raw_data = pd.read_csv('mbti_1.csv')

label = raw_data['type'].tolist()
# # print(label)
#
data_sentence_raw = raw_data['posts'].tolist()
data_sentence_raw = [x[1:-1] for x in data_sentence_raw]
# print(data_sentence_raw[0])
data_sentences_raw = []
for items in data_sentence_raw:
    item = [x for x in items.split('|||')]
    data_sentences_raw.append(item)
#
#
# with open('label.pkl', 'wb') as f:
#   pickle.dump(label, f, pickle.HIGHEST_PROTOCOL)
with open('data_sentences_raw.pkl','wb') as f:
  pickle.dump(data_sentences_raw, f, pickle.HIGHEST_PROTOCOL)

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






with open('data_sentences_raw.pkl', 'rb') as f:
    data_sentences_raw = pickle.load(f)
item_tmp = []
data_sentences_no_http=[]
# data_sentences_with_http=[]
items_tmp = []
for items in data_sentences_raw: # 50
    for item in items: # 1
        item = refine_abbr(item)
        item = remove_number(item)
        item = re.sub("[\.\!\/_,?:\[\]~$%@^#*\-(+\"\')]", "",item)
        for strr in item.split(' '):
            # if len(strr)>0:
            #     item_tmp.append(strr)
            if len(strr)>0 and len(strr)<=4:
                item_tmp.append(strr.lower())
            elif len(strr)>4 and strr[0:4] != 'http':
                item_tmp.append(strr.lower())
        print(item_tmp)
        items_tmp.append(item_tmp)
        item_tmp = []
    data_sentences_no_http.append(items_tmp)
    # data_sentences_with_http.append(items_tmp)
    items_tmp=[]
#
#
with open('data_sentences_no_http_lower.pkl','wb') as f:
  pickle.dump(data_sentences_no_http, f, pickle.HIGHEST_PROTOCOL)
print(data_sentences_no_http)
# with open('data_sentences_with_http.pkl','wb') as f:
#   pickle.dump(data_sentences_with_http, f, pickle.HIGHEST_PROTOCOL)

# with open('data_sentences_no_http.pkl', 'rb') as f:
#     data_sentences_no_http = pickle.load(f)
# print(len(data_sentences_no_http[0]))

# for items in data_sentences_no_http:
#     for item in items:
#         try:
#             str(item)
#             print('success')
#         except:
#             print(item)

