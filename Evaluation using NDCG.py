import math

def DCG(rel):
    sum=0
    for i in range(1,len(rel)):
        sum=sum+(rel[i]/ math.log(i+1, 2))
    sum = sum + rel[0]
    return sum
    
#normalized dcg 
def IDCG(rel):
    rel.sort(reverse=True)
    sum=0
    for i in range(1,len(rel)):
        sum=sum+(rel[i]/ math.log(i+1, 2))
    sum = sum + rel[0]
    return sum

def ndcg(rel):
    i=DCG(rel)
    j=IDCG(rel)
    x=i/j
    return x

#q1=[3,1,3,1,3]
#q2=[1,3,1,1,3]
#q3=[3,3,3,1,3]
#q4=[0,3,3,3,3]
#q5=[3,3,3,3,3]

qmod1=[3,3,1,0,3]
qmod2=[0,0,0,3,0]
qmod3=[3,3,0,0,0]
qmod4=[3,3,3,3,3]
qmod5=[3,3,3,3,3]
q1ex3=[1,3,3,3,3]
q2ex3=[3,3,3,3,1]
q3ex3=[3,3,3,1,0]
q4ex3=[3,3,0,3,1]
print(ndcg(q4ex3))