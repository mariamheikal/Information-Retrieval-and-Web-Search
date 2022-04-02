import json
import time
from operator import pos
from webbrowser import get
import os
path=""
# Opening JSON file
with open(path+'/BiwordIndex.txt') as json_file:
    biword_dict = json.load(json_file)

import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
import re

def binary_search(arr,x):
   l=0
   r=len(arr)-1
   while(l<=r):
      mid=(l+r)//2
      if(arr[mid]==x):
         return True
      elif(x<arr[mid]):
         r=mid-1
      elif(x>arr[mid]):
         l=mid+1
   return False

def binary_intersection(p1,p2,intersection):
    commonl=[]
    for doc1 in p1:
        check=binary_search(p2, doc1)
        if check and intersection:
            commonl.append(doc1)
        elif not check and not intersection:
            commonl.append(doc1)
    return commonl


def getBiwords(text):
    lower_string = text.lower()
    no_number_string = re.sub(r'\d+','',lower_string)
    no_punc_string = re.sub(r'[^\w\s]','', no_number_string)
    no_wspace_string = no_punc_string.strip()
    lst_string = [no_wspace_string][0].split()
    no_stpwords_string=""
    for i in lst_string:
        if not i in stop_words:
            no_stpwords_string += i+' '
    ps = PorterStemmer()
    words = word_tokenize(no_stpwords_string)
    new_words=[]
    w1=''
    w2=''
    for wordindx in range(0,len(words)-1):
        stemmed_word=ps.stem(words[wordindx])
        if wordindx+1<len(words):
            stemmed_word2=ps.stem(words[wordindx+1])
        biword=stemmed_word+" "+stemmed_word2
        new_words.append(biword)
    return new_words


q1='symptoms of bipolar disorder'
q2='common complication of diabetes'
q3='reduce facial nerve inflammation'
q4='symptoms of autism spectrum disorder'
q5='relationship between diabetes and periodontal disease'





def getDocs(q, dict):
    start = time.process_time()
    biwords = getBiwords(q)
    print(biwords)
    post_lists=[]
    url="" #add url path of html files on your local computer
    for bw in biwords:
        if bw in dict:
            post_lists.append(dict[bw][1])

    if len(post_lists)>1:
        p=post_lists[0]
    for i in range(0,len(post_lists)):
        if i+1<len(post_lists):
            p=binary_intersection(p, post_lists[i+1],True)
        i=i+1
    output=''
    your_path = ''
    with open(path+'/docIDs.txt') as json_file:
        dict = json.load(json_file)
    for doc in p:
        f=dict[str(doc)]
        with open(your_path+'/'+f, "r", encoding='utf-8') as ff:
            soup = BeautifulSoup(ff, 'html.parser')
            for data in soup.find_all("p"):
                text=data.get_text()
                if q in text and f not in output:
                    output=output+url+f+'\n'
    print(time.process_time() - start)
    return output


print(getDocs(q1,biword_dict))
print(getDocs(q2,biword_dict))
print(getDocs(q3,biword_dict))
print(getDocs(q4,biword_dict))
print(getDocs(q5,biword_dict))

your_path = path+'/Data Collection/Data'
docIDs={}
docID=0
files = os.listdir(your_path)
for f in files:
    docID=docID+1
    docIDs.update({docID:f})
    print(docID)
json_object = json.dumps(docIDs)
  
# Writing to sample.json
with open(path+"/docIDs.txt","w", encoding="utf-8") as outfile:
    outfile.write(json_object)
outfile.close()