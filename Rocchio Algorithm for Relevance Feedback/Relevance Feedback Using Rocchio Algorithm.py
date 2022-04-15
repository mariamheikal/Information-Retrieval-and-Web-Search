from operator import add 
from nltk.stem import PorterStemmer
import configparser
import time
config = configparser.RawConfigParser()
config.read_file(open("configurations.ini", "r"))
path=config.get('Path','local_path')
print(path)
files_path= path+'/Q5 Docs/'
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def list_unique_terms(query,docs):
    unique = []
    for doc in docs:
        text_file = open(files_path+str(doc)+'.txt', 'r', encoding="utf-8")
        text = text_file.read()
        #cleaning
        text = text.lower()
        words = text.split()
        words = [word.strip('.,!;()[]') for word in words]
        words = [word.replace("'s", '') for word in words]

        #finding unique
        for word in words:
            if word not in unique and word not in stop_words:
                unique.append(word)

    #sort
    
    text = query.lower()
    words = text.split()
    words = [word.strip('.,!;()[]') for word in words]
    words = [word.replace("'s", '') for word in words]
    for word in words:
        if word not in unique and word not in stop_words:
            unique.append(word)

    unique.sort()
    #print
    return unique

def rocchio(query, docs, relv_docs_count):
    start = time.time()
    unique_terms_list=list_unique_terms(query,docs)
    all_docs=[]
    query_vec=[]
    mod_query_vec=[]
    qlist=query.split()
    qvec=False
    added_terms=[]
    for doc in docs:
        doc_vec=[]
        for unique_term in unique_terms_list:
            with open(files_path+str(doc)+'.txt', 'r', encoding="utf-8") as file:
                contents = file.read()
                if unique_term in contents:
                    doc_vec.append(1)
                else:
                    doc_vec.append(0)
            if not qvec:
                if unique_term in qlist:
                    query_vec.append(1)
                else:
                    query_vec.append(0)
        qvec=True
        all_docs.append(doc_vec)
    
    relv_docs_vec= all_docs[0]
    for relv_doc_idx in range(1, relv_docs_count): 
        summed_list = list(map(add, relv_docs_vec, all_docs[relv_doc_idx]))  
        relv_docs_vec=summed_list
    
    non_relv_docs_vec=all_docs[relv_docs_count]
    for non_relv_doc_idx in range(relv_docs_count+1,len(all_docs)):
        summed_list = list(map(add, non_relv_docs_vec, all_docs[non_relv_doc_idx]))  
        non_relv_docs_vec=summed_list
    
    for i in range(0, len(query_vec)):
        rocchio=query_vec[i]+(1/relv_docs_count)*relv_docs_vec[i]-(1/(len(all_docs)-relv_docs_count))*non_relv_docs_vec[i]
        mod_query_vec.append(rocchio)
    added_terms=''
    added_terms_list=[]
    for i in range(0,len(mod_query_vec)):
        if mod_query_vec[i]>0.6:
            added_terms=added_terms+unique_terms_list[i]+' '
            added_terms_list.append(unique_terms_list[i])
    end = time.time()
    print("The time of execution is :", end-start)
    print(len(mod_query_vec))
    print(len(unique_terms_list))
    print(len(added_terms_list))
    return added_terms

q1="symptoms of bipolar disorder"
q2="common complication of diabetes"
q3="reduce facial nerve inflammation"
q4="symptoms of autism spectrum disorder"
q5="relationship between diabetes and periodontal disease"

q1_docs=[9771,9759,9668,49374,46425,46387,42129,9625,40599]
q1_rel_count=5

q2_docs=[22587,3088,3105,3044,3169,37822,46651,43303,44250,670,3120,3041,17377,34544]
q2_rel_count=4

q3_docs=[45787,34638,7195,41321,41803,45786,45780,26633,26633,969,41579,41323,17620]
q3_rel_count=4

q4_docs=[32833,40889,41088,41189,41389,41855,43132,41189,22575,41478,1399,41267,48216]
q4_rel_count=6

q5_docs=[26870,43878,24196,24859,3095,3038,6778,10726,37197,48050]
q5_rel_count=6
print(rocchio(q5,q5_docs,q5_rel_count))
