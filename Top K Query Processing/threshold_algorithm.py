import math
import json
import time
import configparser


config = configparser.RawConfigParser()
config.read_file(open("configurations.ini", "r"))
path=config.get('Settings','path2')
print(path)
prev_asst_path=config.get('Settings','path1')
with open(prev_asst_path+'tf_idf_index') as json_file:
    tfidf_index = json.load(json_file) 

def getDictKeyandValue(d,n): 
    c=0
    mylist=[]
    for i,j in d.items():
        c=c+1
        if c==n:
            mylist=[i,j]
            break
    return mylist 

#Threshold algorithm solves the large buffer size issue with Fagin algorithm 
def threshold_alg(query,k,f,post_lsts):
    start=time.time()
    buffer={}
    all={}
    docsXtfidf_from_seq_access=[]
    res=[]
    num_seq_accesses=0
    num_rand_accesses=0
    query_terms=query.split()
    len_=[]
    all_count_=[]
    threshold=0
    prev_tfidf_values=[0,0,0,0]
    
    for i in range(0,len(post_lsts)):
        len_.append(len(post_lsts[i]))
    
    for j in range(0,max(len_)):
        docsXtfidf_from_seq_access=[]
        threshold=0
        for i in range(0,len(post_lsts)):
        #access docs in these lists sequentially
            if j<len(post_lsts[i]):
                docsXtfidf_from_seq_access.append(getDictKeyandValue(post_lsts[i],j+1))
                num_seq_accesses=num_seq_accesses+1
                
        #now I have the jth doc for every term
                tfidf_sum=0
                if i<len(docsXtfidf_from_seq_access):
                    threshold+=docsXtfidf_from_seq_access[i][1]
                    prev_tfidf_values[i]=docsXtfidf_from_seq_access[i][1]
                    if docsXtfidf_from_seq_access[i][0] not in buffer and len(buffer)<k:
                        for term in query_terms:
                            l=tfidf_index.get(term)
                            if docsXtfidf_from_seq_access[i][0] in l:
                                tfidf_sum=tfidf_sum+l.get(docsXtfidf_from_seq_access[i][0])
                                num_rand_accesses=num_rand_accesses+1
                                if docsXtfidf_from_seq_access[i][0] not in buffer:
                                    buffer.update({docsXtfidf_from_seq_access[i][0]:tfidf_sum})
                                    all.update({docsXtfidf_from_seq_access[i][0]:1})
                                else:
                                    x=all.get(docsXtfidf_from_seq_access[i][0])+1
                                    if x==len(query_terms):
                                        all_count_.append(1)
                                        
                                    all.update({docsXtfidf_from_seq_access[i][0]:x})
                    elif docsXtfidf_from_seq_access[i][0] not in buffer:
                        #compare value of 
                        for term in query_terms:
                            l=tfidf_index.get(term)
                            if docsXtfidf_from_seq_access[i][0] in l:
                                tfidf_sum=tfidf_sum+l.get(docsXtfidf_from_seq_access[i][0])
                                num_rand_accesses=num_rand_accesses+1
                        
                        min_key=min(buffer, key=buffer.get)
                        if buffer.get(min_key)<tfidf_sum:
                            buffer.pop(min_key)
                            buffer.update({docsXtfidf_from_seq_access[i][0]:tfidf_sum})
            else:
                threshold+=prev_tfidf_values[i]
        if threshold<buffer.get(min(buffer, key=buffer.get)):
            end=time.time()
            time_=end-start
            res=[num_seq_accesses, num_rand_accesses, time_]
            json_object = json.dumps(res)
            with open(path+f+query+"_threshold_stats_"+str(k)+"_.txt","w", encoding="utf-8") as outfile:
                outfile.write(json_object)
            outfile.close()
                                    
            return res
    
    end=time.time()
    time_=end-start
    print(time_)
    res=[num_seq_accesses, num_rand_accesses, time_]
    json_object = json.dumps(res)
    with open(path+f+query+"_threshold_stats_"+str(k)+"_.txt","w", encoding="utf-8") as outfile:
            outfile.write(json_object)
    outfile.close()
                                    
    return res







q1="symptom bipolar disord"
q2="common complic diabet"
q3="reduc facial nerv inflamm"
q4="symptom autism spectrum disord"
q5="relationship diabet periodont diseas"
k_list=[5,10,15,20,25,30,35,40,45,50]

l=[]
#o=[]
for term in q1.split():
    docs_list = sorted(tfidf_index.get(term).items(), key=lambda x:x[1], reverse=True)
    sort_docs_dict = dict(docs_list)
    l.append(sort_docs_dict)
for k in k_list:
    print(threshold_alg(q1,k,"Ex2/Q1/",l))
    print('-------------------------------')