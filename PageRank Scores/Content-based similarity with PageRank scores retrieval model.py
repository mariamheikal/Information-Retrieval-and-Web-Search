import json
import time
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import configparser
config = configparser.RawConfigParser()
config.read_file(open("configurations.ini", "r"))
path=config.get('Path','local_path')

with open(path+"/tf_idf_index") as json_file:
    tfidf_index = json.load(json_file) 
with open(path+"/sorted_rankdict.txt") as json_file:
    rank_dict = json.load(json_file) 

stop_words = set(stopwords.words('english'))
def top5(query):
    start = time.time()
    top5=[]
    plists=[]
    docs={}
    words=query.split()
    ps = PorterStemmer()
    for word in words:
        stemmed_word=ps.stem(word)
        if stemmed_word not in stop_words:
            pl=tfidf_index.get(ps.stem(word))
            plists.append(pl)
    for pl in plists:
        if type(pl)==dict:
            for doc in pl:
                if doc not in docs:
                    tfidf_sum=pl.get(doc)
                    for pl2 in plists:
                        if not (pl2==pl) and type(pl2)==dict:
                            if doc in pl2 :
                                tfidf_sum=tfidf_sum+pl2.get(doc)
                    docs.update({doc:tfidf_sum})
    #docs_list = sorted(docs.items(), key=lambda x:x[1], reverse=True)
    #sort_docs_dict = dict(docs_list)
    #print(sort_docs_dict)

    ensemble_scores={}

    #add page rank scores
    for doc,tfidf in docs.items():
        score=rank_dict.get(doc)+tfidf
        ensemble_scores.update({doc:score})
    docs_list = sorted(ensemble_scores.items(), key=lambda x:x[1], reverse=True)
    sort_docs_dict = dict(docs_list)

    for x in list(sort_docs_dict)[0:10]:
        top5.append("Doc {}, tf-idf__&__rank score: {} ".format(x,  sort_docs_dict[x]))
    end = time.time()
    print("The time of execution is :", end-start)
    return top5

q1="symptoms of bipolar disorder"
q2="common complication of diabetes"
q3="reduce facial nerve inflammation"
q4="symptoms of autism spectrum disorder"
q5="relationship between diabetes and periodontal disease"
print(top5(q5))