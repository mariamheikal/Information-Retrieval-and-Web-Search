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




def fagin2(query,k,f,post_lsts):
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
    
    for i in range(0,len(post_lsts)):
        len_.append(len(post_lsts[i]))
    
    for j in range(0,max(len_)):
        docsXtfidf_from_seq_access=[]
        
        for i in range(0,len(post_lsts)):
        #access docs in these lists sequentially
            if j<len(post_lsts[i]):
                docsXtfidf_from_seq_access.append(getDictKeyandValue(post_lsts[i],j+1))
                num_seq_accesses=num_seq_accesses+1
        #now I have the jth doc for every term
                tfidf_sum=0
                if i<len(docsXtfidf_from_seq_access):
                    if docsXtfidf_from_seq_access[i][0] not in buffer:
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
                    else:
                        x=all.get(docsXtfidf_from_seq_access[i][0])+1
                        if x==len(query_terms):
                            all_count_.append(1)
                            
                        all.update({docsXtfidf_from_seq_access[i][0]:x})
              
        
            if len(all_count_)>=k:
                end=time.time()
                time_=end-start
                res=[num_seq_accesses, num_rand_accesses, time_, len(buffer)]
                json_object = json.dumps(res)
                with open(path+f+query+"_fagin_stats_"+str(k)+"_.txt","w", encoding="utf-8") as outfile:
                    outfile.write(json_object)
                outfile.close()
                    
                return res
    
    end=time.time()
    time_=end-start
    print(time_)
    res=[num_seq_accesses, num_rand_accesses, time_, len(buffer)]
    json_object = json.dumps(res)
    with open(path+f+query+"_fagin_stats_"+str(k)+".txt","w", encoding="utf-8") as outfile:
        outfile.write(json_object)
    outfile.close()
                
    return res


q1="symptom bipolar disord"
q2="common complic diabet"
q3="reduc facial nerv inflamm"
q4="symptom autism spectrum disord"
q5="relationship diabet periodont diseas"
k_list=[5,10,15,20,25,30,35,40,45,50]
#,20,25,30,35,40,45,50

l=[]
#o=[]
for term in q5.split():
    docs_list = sorted(tfidf_index.get(term).items(), key=lambda x:x[1], reverse=True)
    sort_docs_dict = dict(docs_list)
    l.append(sort_docs_dict)
for k in k_list:
    print(fagin2(q5,k,"Ex 1/Q5/",l))
    print('-------------------------------')
#for k,v in l[0].items():
#        if k in l[1] and k in l[2] and k in l[3]:
#            o.append(k)
#print(o)








                
                


