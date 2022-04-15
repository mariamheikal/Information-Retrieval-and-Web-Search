import math
import json
from operator import invert
import configparser


config = configparser.RawConfigParser()
config.read_file(open("configurations.ini", "r"))
path=config.get('Path','local_path')
print(path)

with open(path+'/InvertedIndex.txt') as json_file:
    inverted_index = json.load(json_file) 
N=50827


data_path = path+ "/Data Extracted/"
#dft --> doc frequency of the term 
def tf_idf(doc,term, dft):
    tfidf=0
    file = open(doc, "r", encoding="utf-8")
    data = file.read()
    occurrences=data.count(term)
    #print(occurrences)
    tfidf = ( 1 + math.log2(occurrences) )*math.log2(N/dft)
    return tfidf


#Read the inverted index
def build_tfidf_index(inverted_index):
    words_dict={}
    for term, postinglst in inverted_index.items():
        docs_dict={}
        for doc in postinglst[1]:
            file_path=data_path+str(doc)+".txt"
            tfidf=tf_idf(file_path,term,postinglst[0])
            docs_dict.update({doc:tfidf})
        #sort each docs_dist based on the tfidf
        docs_list = sorted(docs_dict.items(), key=lambda x:x[1])
        sort_docs_dict = dict(docs_list)
        words_dict.update({term:sort_docs_dict})
        print(doc)
    return words_dict

words_dict=build_tfidf_index(inverted_index)
json_object = json.dumps(words_dict, indent = 4)
  
#Writing to sample.json
with open(path+"/tf_idf_index","w", encoding="utf-8") as outfile:
    outfile.write(json_object)
outfile.close()

build_tfidf_index(inverted_index)
