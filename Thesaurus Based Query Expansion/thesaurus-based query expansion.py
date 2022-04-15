import configparser
import json
import os
import time
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import nltk
import numpy as np
config = configparser.RawConfigParser()
config.read_file(open("configurations.ini", "r"))
path=config.get('Path','local_path')

from nltk.corpus import stopwords
with open(path+'/InvertedIndex.txt') as json_file:
    inverted_index = json.load(json_file) 
stop_words = set(stopwords.words('english'))
your_path = 'C:/Users/Data Collection/Data/' #html files path
files = os.listdir(your_path)

N=50827
M=len(inverted_index)
unique_wordXdoc={}
def get_unique_words():
    docID=0
    for f in files:
        docID=docID+1
        with open(your_path+'/'+f, "r", encoding='utf-8') as ff:
            soup = BeautifulSoup(ff, 'html.parser')
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
                no_stpwords_string = no_stpwords_string[:-1]
                words = word_tokenize(no_stpwords_string)
                for word in words:
                    if word[0:4]!='http':  
                        if word not in unique_wordXdoc:
                            lst=[docID]
                            unique_wordXdoc.update({word:lst})
                        else:
                            lst = unique_wordXdoc[word]
                            if docID not in lst:
                                lst.append(docID)
                                unique_wordXdoc.update({word:lst})
        print(docID)                        

    return unique_wordXdoc


#UNCOMMENT - RUN ONCE -----------------------------------------------------------------

#unique_words=get_unique_words()

 
#json_object = json.dumps(unique_words, indent = 4)
  
# Writing to sample.json
#with open(path+"/unique_words.txt","w", encoding="utf-8") as outfile:
#    outfile.write(json_object)
#outfile.close()

#---------------------------------------------------------------------------------------

with open(path+'/unique_words.txt') as json_file:
    terms_index = json.load(json_file) 

def build_term_doc_incidence_matrix(terms_index):
    start = time.time()
    a_mat=[]
    m=0
    
    for term, doc_list in terms_index.items():

        term_list=[0]*50827
        for doc in doc_list:
            if doc>0:
                term_list[doc-1]=1
        m=m+1
    
        print(m)
        a_mat.append(term_list)
    aT_mat=np.array(a_mat)
    aT_mat.transpose()
    result = [[sum(a * b for a, b in zip(A_row, B_col))
                        for B_col in zip(*a_mat)]
                                for A_row in aT_mat]
    end = time.time()
    print("The time of execution is :", end-start)
    
    json_object = json.dumps(aT_mat)
    with open(path+"/aT_matrix.txt","w", encoding="utf-8") as outfile:
        outfile.write(json_object)
    outfile.close()
    json_object = json.dumps(result)
    with open(path+"/c_matrix.txt","w", encoding="utf-8") as outfile:
        outfile.write(json_object)
    outfile.close()

    return a_mat

#UNCOMMENT - RUN ONCE -----------------------------------------------------------------
  
#a_mat=build_term_doc_incidence_matrix(terms_index)
#json_object = json.dumps(a_mat)
#with open(path+"/a_matrix.txt","w", encoding="utf-8") as outfile:
#    outfile.write(json_object)
#outfile.close()
#---------------------------------------------------------------------------------------


with open(path+'/InvertedIndex.txt') as json_file:
    c_matrix = json.load(json_file) 