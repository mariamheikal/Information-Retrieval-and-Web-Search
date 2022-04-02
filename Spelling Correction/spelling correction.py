import json 
from difflib import get_close_matches
import nltk
from nltk.corpus import stopwords
from itertools import product as pd
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words('english'))

from rapidfuzz.distance import Levenshtein

path=""
with open(path+'/DictionaryOfWords.txt') as json_file:
    wordsdict = json.load(json_file)



def getEditWords(q,dict):
    edit_words={}
    q_list=q.split()
    for w in q_list:
        for w2 in dict:
            if w not in stop_words and Levenshtein.distance(w,w2)<=2 and (w[0]=='t' and w2[0]=='s' or w[0]==w2[0]):
                if w not in edit_words:
                    edit_words.update({w:[w2]})
                else:
                    words=edit_words[w]
                    words.append(w2)
                    edit_words.update({w:words})
        #l=get_close_matches(w, edit_words[w])
        #closest_edit_words.update({w:l})
    return edit_words
                
def getAlternativeQueries(q):
    start = time.process_time()
    dict_alt=getEditWords(q,wordsdict)
    
    i=0 
    l=[]
    q_split=q.split()
    for qw in q_split:
        if qw not in stop_words:
            l.append(qw)
    s1=dict_alt[l[0]]
    for k in range(len(l)):
        if k+1<len(dict_alt):
            s1 = [ i+' '+j for i, j in pd(s1, dict_alt[l[k+1]])]
    print(time.process_time() - start)
    return s1

with open(path+'/BiwordIndex.txt') as json_file:
    biword_dict = json.load(json_file)

org_q1='meditation overdus headachse'
spell_mis_q1='meditation overdus headachse'

org_q2='symptoms of bipolar disorder'
spell_mis_q2='teech dekau'

org_q3='risk of developing diabetes'
spell_mis_q3='redk of dwvelopinh diabetise'

org_q4='misalighnmnt of the teeth'
spell_mis_q4='misalighnmnt of the eyeth'

org_q5='complementary health practices'
spell_mis_q5='complwmentery hesltg pracyicea'




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
    for wordindx in range(0,len(words)-1):
        stemmed_word=ps.stem(words[wordindx])
        if wordindx+1<len(words):
            stemmed_word2=ps.stem(words[wordindx+1])
        biword=stemmed_word+" "+stemmed_word2
        new_words.append(biword)
    return new_words





import time 


def getDocs(q, dict):
    biwords = getBiwords(q)
    post_lists=[]
    url="" #add url path of your html files on your local machine
    for bw in biwords:
        if bw in dict:
            post_lists.append(dict[bw][1])
    output=[]
    if len(post_lists)>1:
        p=post_lists[0]
        for i in range(0,len(post_lists)):
            if i+1<len(post_lists):
                p=binary_intersection(p, post_lists[i+1],True)
            i=i+1
        
        your_path = '/Data Collection/Data'
        with open(path+'/docIDs.txt') as json_file:
            dict = json.load(json_file)
        for doc in p:
            f=dict[str(doc)]
            with open(your_path+'/'+f, "r", encoding='utf-8') as ff:
                soup = BeautifulSoup(ff, 'html.parser')
                for data in soup.find_all("p"):
                    text=data.get_text()
                    if q in text and f not in output:
                        output.append(url+f)
    elif len(post_lists)==1:
        your_path = path+'/Data Collection/Data'
        with open(path+'/docIDs.txt') as json_file:
            dict = json.load(json_file)
        for doc in post_lists[0]:
            f=dict[str(doc)]
            with open(your_path+'/'+f, "r", encoding='utf-8') as ff:
                soup = BeautifulSoup(ff, 'html.parser')
                for data in soup.find_all("p"):
                    text=data.get_text()
                    if q in text and f not in output:
                        output.append(url+f)

    return output

def getQuriesDocs(edits, dict):
    q_dict={}
    for q in edits:
        qs=q.split()
        qsl=qs[0]+' '+qs[1]+' '+qs[2]
        l=getDocs(qsl,dict)
        q_dict.update({qsl:len(l)})
    return q_dict
########### -------------------------- DONE ------------------------------ ####################
edits=getAlternativeQueries(spell_mis_q1)
qdict=getQuriesDocs(edits,biword_dict)
import json
json_object = json.dumps(qdict, indent = 4)
with open(path+"/q5.txt","w", encoding="utf-8") as outfile:
    outfile.write(json_object)
outfile.close()
print(Levenshtein.distance('decay','dekau'))
print(Levenshtein.distance('delay','dekau'))
########## --------------------------------------------------------------- #####################

from nltk import ngrams
from nltk.stem import PorterStemmer
def getTrigrams(text):
    trigrams={}
    lower_string = text.lower()
    no_number_string = re.sub(r'\d+','',lower_string)
            # remove all punctuation except words and space
    no_punc_string = re.sub(r'[^\w\s]','', no_number_string)
            # remove white spaces
    no_wspace_string = no_punc_string.strip()
    lst_string = [no_wspace_string][0].split()
            # remove stopwords
    no_stpwords_string=""
    for i in lst_string:
        if not i in stop_words:
            no_stpwords_string += i+' '
            # removing last space
    no_stpwords_string = no_stpwords_string[:-1]
    words = word_tokenize(no_stpwords_string)
    for word in words:
        triword =  [""+t[0]+t[1]+t[2] for t in nltk.trigrams(word)]
        trigrams.update({word:triword})
    
    return  trigrams 

def getTrigramsDict(words_dict):
    trigram_dict={}
    for w in words_dict:
        triword =  [""+t[0]+t[1]+t[2] for t in nltk.trigrams(w)]
        trigram_dict.update({w:triword})
    return trigram_dict

def jaccard(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union


def getAlternativeQueries_trigrams(q):
    start = time.process_time()
    with open(path+'/WordsTrigrams.txt') as json_file:
        words_trigram_dict = json.load(json_file)
    q_trigrams_dict=getTrigrams(q)
    qwords=[]
    termsvswords={}
    for term in q_trigrams_dict:
        qwords.append(term)
        wordsVSjc={}
        #get Jaccard coffecient bet trigram set of the query term and collection term
        for word in words_trigram_dict:
            if word[0]==term[0]:
                q_term_trigrams = q_trigrams_dict[term]
                dict_word_trigram = words_trigram_dict[word]
                jc=jaccard(q_term_trigrams,dict_word_trigram)
                wordsVSjc.update({word:jc})
        termsvswords.update({term:wordsVSjc})
    
    #return termsvswords
        
    #sort the dict and get the top 2 terms foe each query term
    top2edits={}
    for term in termsvswords:
        termsVSjc=termsvswords[term]
        jclist = sorted(termsVSjc.items(), key=lambda x:x[1], reverse=True)
        sortdict = dict(jclist)
        l=[]
        for i in list(sortdict)[0:2]:
            l.append(i)
        top2edits.update({term:l})
    s1=top2edits[qwords[0]]
    for windx in range(0,len(top2edits)):
        if windx+1<len(top2edits):
             s1 = [ i+' '+j for i, j in pd(s1, top2edits[qwords[windx+1]])]
    print(time.process_time() - start)
    return top2edits
    


qdict=getTrigramsDict(wordsdict)
import json
json_object = json.dumps(qdict, indent = 4)
with open(path+"/WordsTrigrams.txt","w", encoding="utf-8") as outfile:
    outfile.write(json_object)
outfile.close()


print(getAlternativeQueries_trigrams(spell_mis_q3))











    

