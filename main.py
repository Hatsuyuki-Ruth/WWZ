# -*- coding: utf-8 -*-

import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
from myconfig import Config
from model import myDPCNN
import jieba
import re
#from data import TextDataset
import argparse
import numpy as np
import re
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
TrainFile = 'data/train_with_label.txt'
TestFile = 'data/test_with_label.txt'
vector_dic = 'data/vector.model.txt'
vec_out='data/batch_vector.txt'
outp1='data/text8.model'
class TextDataset(data.Dataset):

    def __init__(self,File):
        input_file=open(File, encoding='utf8')
        lines = input_file.readlines()
        self.train_set = [line.strip().split('\t')[0] for line in lines]
        self.labels = [line.strip().split('\t')[-1] for line in lines]

    def __getitem__(self, index):
        return self.train_set[index], self.labels[index]

    def __len__(self):
        return len(self.train_set)
    
torch.manual_seed(1)

parser = argparse.ArgumentParser()
parser.add_argument('--lr', type=float, default=0.001)
parser.add_argument('--batch_size', type=int, default=16)
parser.add_argument('--epoch', type=int, default=10)
parser.add_argument('--gpu', type=int, default=0)
parser.add_argument('--out_channel', type=int, default=2)
parser.add_argument('--label_num', type=int, default=2)
parser.add_argument('--seed', type=int, default=1)
parser.add_argument('--word_embedding_dimension', type=int, default=200)
args = parser.parse_args()


torch.manual_seed(args.seed)##为当前GPU设置随机种子

if torch.cuda.is_available():
    torch.cuda.set_device(args.gpu)

# Create the configuration
config = Config(sentence_max_size=50,
                batch_size=args.batch_size,
                word_num=100000,
#                label_num=args.label_num,
                learning_rate=args.lr,
                cuda=args.gpu,
                epoch=args.epoch,
                word_embedding_dimension=args.word_embedding_dimension)

training_set = TextDataset(TrainFile)
length=len(training_set)
training_iter = data.DataLoader(dataset=training_set,
                                batch_size=config.batch_size,
                                num_workers=0)


model = myDPCNN.DPCNN(config)##一个net
#embeds = nn.Embedding(config.word_num, config.word_embedding_dimension)
#embeds.weight.data.copy_(torch.from_numpy(pretrained_embeddings))
# if torch.cuda.is_available():
#     model.cuda()
#     embeds = embeds.cuda()

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=config.lr)
list_intentions = ["INTJ","ESFP", "INTP", "INFJ", "INFP", "ISTJ",
                       "ISTP", "ISFJ", "ISFP", "ESTJ", "ESTP",
                       "ESFJ", "ENTJ", "ENTP", "ENFJ", "ENFP"]
label_types=len(list_intentions)
dic_label={list_intentions[x]:x for x in range(label_types)}
def label_vector(label):
    batch=len(label)
    label_matrix=np.zeros(batch)
    for i in range(batch):
        label_matrix[i]=dic_label[label[i].strip().replace("__label__","")]
    return torch.from_numpy(label_matrix)

def vecor_dic(TrainFile,outp1,vector_dic):
    model = Word2Vec(LineSentence(TrainFile), size=config.word_embedding_dimension, window=1, min_count=1)
    model.save(outp1)
    model.wv.save_word2vec_format(vector_dic+ '.model.txt',  binary=False)
    
def corpus_vector(corpus_name,vector_dic,vec_out):
    batch=corpus_name
    h=open(vector_dic,'r',encoding='utf8')
    matrix=np.zeros((len(batch),1,config.word_num,config.word_embedding_dimension))
    dic_label={line.split()[0]:line.split()[1:] for line in h.readlines()}
    for i in range(len(batch)):
        for j in range(len(batch[i])):
            if batch[i][j] in dic_label.keys():
                matrix[i][0][j]=dic_label[batch[i][j]]
                
    h.close()
    return matrix


vecor_dic(TrainFile,outp1,vector_dic)
count = 0
loss_sum = 0
file_path=''
#Train the model
#model=torch.load('./train_res/ver1.ckpt')
for epoch in range(config.epoch):
   for text_data, label in training_iter:
       label=label_vector(label).type(torch.LongTensor)   ## word to vector
       if config.cuda and torch.cuda.is_available():
           data = data.cuda()
           label = label.cuda()
       data=torch.from_numpy(corpus_vector(text_data,vector_dic,vec_out))
       data=data.type(torch.FloatTensor)
       out = model(data)
       loss = criterion(out, autograd.Variable(label))

       loss_sum += loss.item()
       count += 1

       if count % 100 == 0:
           print("epoch", epoch, end='  ')
           print("The loss is: %.5f" % (loss_sum/100))

           loss_sum = 0
           count = 0

       optimizer.zero_grad()###梯度置零
       loss.backward()
       optimizer.step()
   # save the model in every epoch
torch.save(model,'./train_res/ver1.ckpt')

##test
model=torch.load('./train_res/ver1.ckpt')
test_set = TextDataset(TestFile)
length=len(test_set)
test_iter = data.DataLoader(dataset=test_set,
                                batch_size=config.batch_size,
                                num_workers=0)
cor_count=0
tot_count=0
for text_data, label in test_iter:
     label=label_vector(label).type(torch.LongTensor)   ## word to vector
     if config.cuda and torch.cuda.is_available():
         data = data.cuda()
         label = label.cuda()
     test_data=torch.from_numpy(corpus_vector(text_data,vector_dic,vec_out)).type(torch.FloatTensor) 
     test_out=model.predict(test_data)
     res=torch.eq(label,test_out).numpy()
     cor_count +=np.sum(res)
     tot_count +=res.size
print('precsion:',cor_count/tot_count)
        
    