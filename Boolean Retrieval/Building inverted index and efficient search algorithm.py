import os
#import pip
import re

# importing modules
#------------Imports
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
path=""
stop_words = set(stopwords.words('english'))
data_path = path+'/Data Collection/Data'
files = os.listdir(data_path)
docID=0
words_dict={}
wordsVsStem={}
def linear_intersection(p1,p2):
    commonl=[]
    for doc1 in p1:
        for doc2 in p2:
            if doc1==doc2 and doc1 not in commonl:
                commonl.append(doc1)
    return commonl

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

def binary_intersection(p1,p2):
    commonl=[]
    for doc1 in p1:
        if binary_search(p2, doc1):
            commonl.append(doc1)
    return commonl

from math import sqrt

def skip_intersection(p1,p2):
    commonl=[]
    skip1=sqrt(len(p1))
    skip2=sqrt(len(p2))
    doc1i=0
    doc2i=0
    while (doc1i <len(p1)):
        while (doc2i <len(p2)):
            if p1[doc1i]==p2[doc2i] and p1[doc1i] not in commonl:
                commonl.append(p1[doc1i])
                doc1i=doc1i+1
                doc2i=doc2i+1
            elif p1[doc1i]<p2[doc2i]:
                if doc1i+skip1<len(p1) and p1[doc1i+skip1]<=p2[doc2i]:
                    doc1i=doc1i+skip1-1
                elif doc2i+skip2<len(p2) and p2[doc2i+skip2]<=p1[doc1i]:
                    doc2i=doc2i+skip2-1

    return commonl


#-------------------------- Creating the inverted index ------------ words_dict --------------------------------------------------
for f in files:
    docID=docID+1
    with open(data_path+'/'+f, "r", encoding='utf-8') as ff:
        soup = BeautifulSoup(ff, 'html.parser')
        file = open(path+"/Data Extracted/"+str(docID)+".txt","w", encoding="utf-8")
        # traverse paragraphs from soup
        for data in soup.find_all("p"):
            #extract text
            text=data.get_text()
            #file.write(text + "\n")
            #normalize text in list 
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
            file.write(no_stpwords_string+ "\n")
            no_stpwords_string = no_stpwords_string[:-1]
            ps = PorterStemmer()
            words = word_tokenize(no_stpwords_string)
            for word in words:
                if word[0:4]!='http':  
                    stemmed_word=ps.stem(word)
                    if stemmed_word not in words_dict:
                        lst=[1,[docID]]
                        wordsVsStem.update({word:stemmed_word})
                        words_dict.update({stemmed_word:lst})
                    else:
                        lst = words_dict[stemmed_word]
                        if docID not in lst[1]:
                            lst[0]=lst[0]+1
                            lst[1].append(docID)
                            words_dict.update({stemmed_word:lst})
    file.close()
    print(docID)
sorted_word_dic={}
for i in sorted(words_dict):
   sorted_word_dic[i]=words_dict[i]
import json 
# Serializing json 
json_object = json.dumps(sorted_word_dic, indent = 4)
  
# Writing to sample.json
with open(path+"/InvertedIndex.txt","w", encoding="utf-8") as outfile:
    outfile.write(json_object)
outfile.close()
#-----------------------------------------------------------------------------------------------------------------------------------------


no_terms=0
hist_dict={}
for key, value in sorted_word_dic.items():
        if value[0] not in hist_dict:
            hist_dict.update({value[0]:1})
        else:
            freq=hist_dict.get(value[0])
            print(freq)
            freq=freq+1
            hist_dict.update({value[0]:freq})
sorted_hist_dic={}
for i in sorted(hist_dict):
   sorted_hist_dic[i]=hist_dict[i]
print(sorted_hist_dic)



json_object = json.dumps(sorted_hist_dic, indent = 4)
  
# Writing to sample.json
with open(path+"/Histogram.txt","w", encoding="utf-8") as outfile:
    outfile.write(json_object)
outfile.close()

#-------------------------------------------------------------------------------------------------------------------
distinct_words_num=len(sorted_word_dic)
num_docs=docID
cum_freq=0
for key, value in sorted_word_dic.items():
    cum_freq=cum_freq+value[0]
avg_distinct_words=cum_freq/distinct_words_num

docs_wrd_count={}
for key, value in sorted_word_dic.items():
    if key not in docs_wrd_count:
        docs_wrd_count.update({key:1})
    else:
        count_wrd=docs_wrd_count.get(key)
        count_wrd=count_wrd+1
        docs_wrd_count.update({key:count_wrd})
cumsum=0
c=0
for key, value in docs_wrd_count.items():
    cumsum= cumsum+value
    c=c+1
avg=cumsum/c
file = open(path+"/Stats.txt","w", encoding="utf-8")
file.write("Number of distinct words" + "\t" + str(distinct_words_num) + "\n")
file.write("Number of indexed documents" + "\t" + str(num_docs) + "\n")
file.write("Average number of distinct words per document" + "\t" + str(avg_distinct_words) + "\n")
file.write("Cum sum of distinct words per document" + "\t" + str(cumsum) + "\n")
file.write("Average distinct words per document" + "\t" + str(avg) + "\n")


file.close()

#file = open("C:/Users/Mariam Safieldin/Documents/AUB/Semester 2/CMPS 391/Assignment 1 - Data Collection/Assign2_Ex1_InvertedIndex.txt","w", encoding="utf-8")
#for key, value in sorted_word_dic.items():
#    file.write(key + "\t" + str(value) + "\n")
#file.close()


#-------------------------------------------------------------------------------------------------------------------
import string
letter_dict = dict( (key, []) for key in string.ascii_lowercase )

for key, value in sorted_word_dic.items():
    val=letter_dict.get(key[0]) #list of docID starting with letter 
    if val != None:
        val.extend(value[1])
        letter_dict.update({key[0]:val})
#remove duplicates from letter lists
for key, value in letter_dict.items():
    no_dup_value = list(dict.fromkeys(value))
    letter_dict.update({key:no_dup_value})
   
# Serializing json 
json_object = json.dumps(letter_dict, indent = 4)
  
# Writing to sample.json
with open(path+"LetterLists.txt","w", encoding="utf-8") as outfile:
    outfile.write(json_object)
outfile.close()
#-------------------------------------------------------------------------------------------------------------------------------
#Intersection Algorithm:   ------ I am looking for docs that start with both a and b ... a and c ... 

import time
start = time.time()
#file = open("C:/Users/Mariam Safieldin/Documents/AUB/Semester 2/CMPS 391/Assignment 1 - Data Collection/Assign2_Ex2_Exec_Time.txt","w", encoding="utf-8")
elem_count=0
for key, value in letter_dict.items():
    posting_list=value
    for key2, value2 in letter_dict.items():
        if key!=key2:
            #file.write(key + "\t" + key2 + "\t" + str(len(value)) +  "\t" + str(len(value2)) + "\n")
            elem_count=elem_count+len(value)+len(value2)
            intersection=linear_intersection(value,value2)
        else:
            print("EQUAL")
end = time.time()
#file.close()
exectime = end-start
file = open(path+"/Exec_Time.txt","w", encoding="utf-8")
file.write("Number of elements:" + "\t" + str(elem_count) +  "\n")
file.write("Linear Intersection Algorithm Execution Time:" + "\t" + str(exectime) +  "\n")

#Efficient Intersection Algorithm ----------- Binary Search -------------------------------
start = time.time()
elem_count=0
for key, value in letter_dict.items():
    posting_list=value
    for key2, value2 in letter_dict.items():
        if key!=key2:
            elem_count=elem_count+len(value)+len(value2)
            intersection=binary_intersection(value,value2)
end = time.time()
exectime = end-start
file.write("Number of elements:" + "\t" + str(elem_count) +  "\n")
file.write("Skip Intersection Algorithm Execution Time:" + "\t" + str(exectime) +  "\n")
file.close()

