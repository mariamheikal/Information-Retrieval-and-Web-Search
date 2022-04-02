import json
from nltk.stem import PorterStemmer
import time
import numpy as np

path=""

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


# Opening JSON file
with open(path+'/InvertedIndex.txt') as json_file:
    dict = json.load(json_file)

q1='insulin AND hypoglycemia'
q2='breast AND cancer NOT heart'
q3='breastfeeding OR (risk AND nonbreastfeeding)'
q4='recommendation AND health'
q5='(coughing OR fever) AND mask'
#first stem the words, locate all the keys, and get their values
def queryAnswerer_helper(dict,q):
    q_split=q.split()
    ps = PorterStemmer()
    out=[]
    for i in range(0,len(q_split)):
        if q_split[i][0]!='(':
            l1=dict.get(ps.stem(q_split[i]))[1]
            if i+2<len(q_split) and q_split[i+2][0]!='(':
                l2=dict.get(ps.stem(q_split[i+2]))[1]
                if q_split[i+1]=='OR':
                    out=np.unique(l1 + l2)
                elif q_split[i+1]=='AND':
                    out=binary_intersection(l1,l2, True)
                elif q_split[i+1]=='NOT':
                    out =binary_intersection(l1,l2,False)
    return out 

def queryAnswerer(dict, q):
    start = time.process_time()
    q_split=q.split()
    op=['OR','AND','NOT']
    ps = PorterStemmer()
    out_sofar=[]
    out=[]
    skip=False
    i=0
    while i<len(q_split):
        if q_split[i][0]!='(':
            if q_split[i] not in op:
                l1=dict.get(ps.stem(q_split[i]))[1]
                if i+2<len(q_split) and q_split[i+2][0]!='(':
                    l2=dict.get(ps.stem(q_split[i+2]))[1]
                    if q_split[i+1]=='OR':
                        out=np.unique(l1 + l2)
                    elif q_split[i+1]=='AND':
                        out=binary_intersection(l1,l2, True)
                    elif q_split[i+1]=='NOT':
                        out =binary_intersection(l1,l2,False)
                else:
                    if i+2<len(q_split) and q_split[i+2][0]=='(':
                        j=1
                        q=q_split[i+2]
                        while i+2+j<len(q_split) and q_split[i+2+j][-1]!=')':
                            q=q+' '+q_split[i+2+j]
                            j=j+1
                        if i+2+j<len(q_split):
                            q=q+' '+q_split[i+2+j]
                        skip=True
                        j=j+2
                        q=q[1:-1]
                        l2=queryAnswerer_helper(dict,q)
                        out = boolean_op(q_split[i+1],l1,l2)
            else:
                if i+1<len(q_split) and q_split[i+1][0]!='(':
                    l2=dict.get(ps.stem(q_split[i+1]))[1]
                    if q_split[i]=='OR':
                        out=np.unique(out_sofar + l2)
                    elif q_split[i]=='AND':
                        out=binary_intersection(out_sofar,l2, True)
                    elif q_split[i]=='NOT':
                        out =binary_intersection(out_sofar,l2,False)
                else:
                    if i+1<len(q_split) and q_split[i+1][0]=='(':
                        j=1
                        q=q_split[i+2]
                        while i+1+j<len(q_split) and q_split[i+1+j][-1]!=')':
                            q=q+' '+q_split[i+1+j]
                            j=j+1
                        if i+1+j<len(q_split):
                            q=q+' '+q_split[i+1+j]
                        skip=True
                        j=j+1
                        q=q[1:-1]
                        l2=queryAnswerer_helper(dict,q)
                        out = boolean_op(q_split[i+1],out_sofar,l2)

        else:
            q=q_split[i]
            j=1
            while i+j<len(q_split) and q_split[i+j][-1]!=')':
                q=q+' '+q_split[i+j]
                j=j+1
            if i+j<len(q_split):
                q=q+' '+q_split[i+j]
            skip=True
            q=q[1:-1]
            l2=queryAnswerer_helper(dict,q)
            out = l2 #boolean_op(q_split[i+1],out_sofar,l2)

        if skip:
            i=i+1+j
        else:
            i=i+2
        out_sofar=out
    print(time.process_time() - start)
    return out_sofar

def boolean_op(bool,p1,p2):
    if bool=='OR':
        return np.unique(p1 + p2)
    elif bool=='AND':
        return binary_intersection(p1,p2, True)
    elif bool=='NOT':
         return binary_intersection(p1,p2,False)
    

    
#file.close()
queryAnswerer(dict, q3)
