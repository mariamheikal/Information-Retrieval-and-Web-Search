import networkx as nx
import bs4
import configparser
import json
import time 
import os
from collections import Counter
import glob
from bs4 import BeautifulSoup
import os
import collections
import configparser
config = configparser.RawConfigParser()
config.read_file(open("configurations.ini", "r"))
path=config.get('Path','local_path')
with open(path+'/docsIndexes.txt') as json_file:
    docs_index = json.load(json_file) 
your_path = 'C:/Users/Data Collection/Data'
files = os.listdir(your_path)
with open(path+'/dic_pagerank.txt') as json_file:
    dic = json.load(json_file) 

C=dict()
R=dict()
E=dict()
docs_nb = len(dic)
alpha=0.15
for p in dic:
    E[p]= 1/docs_nb
    R[p]= 1/docs_nb
    C[p]=0
prev_summation=10
sum2=0
j=1
start=time.time()
w=False
while abs(prev_summation-sum2)>0.2:
    
    print("Iteration:",j)
    print('----------------------')
    print(abs(prev_summation-sum2))
    prev_summation=sum2
    for p in dic:
        print(p)
        c=0
        #print("Page id:",p)
        summation=0
        for q in dic:
            
            mylist = dic[q]
            count = 0
            x= int(p)
           
            if x in mylist:
                print(q)
                print(x)
                count=count+1
                c=c+1
                
            if count!=0:
                summation+=R[q]/len(mylist)
    
        C[p]=c
        R[p]=(1-alpha)*summation + alpha*E[p]
    summation2=0
    values = R.values()
    summation2=sum(values)
    c=1/summation2
    #normalize
    for p in dic:
        R[p]=c*R[p]
    values = R.values()
    sum2=sum(values)
    if w==False:
        json_object = json.dumps(C)
        with open(path+"/count.txt","w", encoding="utf-8") as outfile:
            outfile.write(json_object)
        outfile.close()
        w=True
    
    j=j+1

    
    if j==3:
        break
end=time.time()
t=end-start
l=[t,j]
json_object = json.dumps(l)
with open(path+"/time_poweriter.txt","w", encoding="utf-8") as outfile:
    outfile.write(json_object)
outfile.close()

r_list=[]
ranks={}
docId=0
for r in R:
    docId=docId+1
    ranks.update({docId:R[r]})
    r_list.append([r,R[r]])

sorted_r=sorted(r_list,key=lambda r_list:r_list[1], reverse=True)

json_object = json.dumps(sorted_r)
with open(path+"/sorted_ranklist.txt","w", encoding="utf-8") as outfile:
    outfile.write(json_object)
outfile.close()
docs_list = sorted(ranks.items(), key=lambda x:x[1], reverse=True)
sort_ranks_dict = dict(docs_list)
json_object = json.dumps(sort_ranks_dict)
with open(path+"/sorted_rankdict.txt","w", encoding="utf-8") as outfile:
    outfile.write(json_object)
outfile.close()


for i in range(10):
    print("Page Ranking:",str(i+1))
    print("Page:",dic[sorted_r[i][0]])
    print("Page Rank Value:",sorted_r[i][1])
    print("______________________________________________")

import json 
# Serializing json 
json_object = json.dumps(sorted_r, indent = 4)
  
# Writing to sample.json
with open(path+"/page_rank.txt","w", encoding="utf-8") as outfile:
    outfile.write(json_object)
outfile.close()