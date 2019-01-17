import re
import pickle

celebratity=dict()
with open('celebratity.txt','r') as f:
    content = f.readlines()
    for item in content:
        name,content = item.split('\t')
        celebratity[name]=content

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

def sentences_to_words(sentences):
    sentences=refine_abbr(sentences)
    sentences=remove_number(sentences)
    sentences = re.sub("[\.\!\/_,?:\[\]~$%@^#*\-(+\"\')]", "", sentences)
    words = [word.lower() for word in sentences.split(' ') if word!='']
    words = ' '.join(words)
    return words

# print(sentences_to_words(celebratity['Tom Cruise']))

celebratity_type=dict()
import fastText

model_name='model/'+'classify_with_videos'+'.model'
type_set = ['ISTJ','ISFJ','INFJ','INTJ','ISTP','ISFP','INFP','INTP','ESTP','ESFP','ENFP','ENTP','ESTJ','ESFJ','ENFJ','ENTJ']


classifier = fastText.load_model(model_name)
count=0
for name in celebratity.keys():
    count+=1
    words=sentences_to_words(celebratity[name])
    print(words)
    words=words.replace('\n','')
#    with open('words%d.txt'%count,'w') as f:
#        f.write('i love you')
    results = classifier.predict(words,16)
    print(name, results)
    type, proba = results
    real_type = type[0][-4:]
    print(real_type)
    type = [item[-4:] for item in type]
    proba = [item for item in proba]
    res = dict(zip(type,proba))
    vec = [res[type] for type in type_set]
    celebratity_type[name]=(real_type,vec)

print(celebratity_type)
with open('celebratity_type.pkl','wb') as f:
    pickle.dump(celebratity_type, f, pickle.HIGHEST_PROTOCOL)








