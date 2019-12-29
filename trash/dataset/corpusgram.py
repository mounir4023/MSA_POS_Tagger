from lxml import etree
import re
import nltk
import pickle

def GetBigT(t1):

    for t in Tbig:
        if(t.startswith(t1+"|")):
            print(t+"=="+str(Tbig[t]))
def GetTriT(t1,t2):

    for t in Ttri:
        if(t.startswith(t1+"|"+t2+"|")):
            print(t+"=="+str(Ttri[t]))
root = etree.parse("corpus.xml")
sents = [ ]
words=[]
for s in root.xpath("/CORPUS/Phrase"):
    tokens = re.sub(r'\s+',' ',s[2].text)
    tags = re.sub(r'\s+',' ',s[3].text)
    sents.append({
            'num':s[0].text,
            'len':s[5].text,
            'raw':s[1].text,
            'tokens':tokens.split(" "),
            'tags':tags.split(" "),
        })
NU=0
for s in sents[:100]:
    
    s["tokens"][0:0] = ['<START>']
for s in sents[:100]:
    for t in s["tokens"]:
        if t == '' or t == ' ':
            s["tokens"].remove(t)
        else:
            words.append(t)
            NU+=1
    for t in s["tags"]:
        if t == '' or t == ' ':
            s["tags"].remove(t)


words=set(words)
matUni=nltk.FreqDist()
UniFreq=nltk.FreqDist()
for s in sents[:100]:
    for word in s["tokens"]:
        matUni[word]+=(1/NU)
        UniFreq[word]+=1

NB=0
MatBig=nltk.FreqDist()
BigFreq=nltk.FreqDist()
for s in sents[:100]:
    prev=s["tokens"][0]
    i=0
    for word in s["tokens"]:
        if(i!=0):
            MatBig[prev+"|"+ word]+=(1/UniFreq[prev])
            BigFreq[prev+"|"+ word]+=1
            prev=word
        else:
            i=1
"""
print("---Bigrams")
for w in MatBig:
    print(w+"="+str(MatBig[w]))
"""
#starts calculating the trigrams using the freqq of the bigrams
MatTri=nltk.FreqDist()
for s in sents[:100]:
    prevp=s["tokens"][0]
    prevn=s["tokens"][1]
    i=0
    for word in s["tokens"]:
        if(i>1):
            MatTri[prevp+"|"+prevn+"|"+ word]+=(1/BigFreq[prevp+"|"+prevn])
            prevp=prevn
            prevn=word
        else:
            i+=1
"""
print("---Trigrams")
for w in MatTri:
    print(w+"="+str(MatTri[w]))
"""
Tuni=nltk.FreqDist()
TUniFreq=nltk.FreqDist()
for s in sents[:100]:

    for word in s["tags"]:
        Tuni[word]+=(1/NU)

        TUniFreq[word]+=1

NB=0
Tbig=nltk.FreqDist()
TBigFreq=nltk.FreqDist()
for s in sents[:100]:
    prev=s["tags"][0]
    i=0
    for word in s["tags"]:
        if(i!=0):
            Tbig[prev+"|"+ word]+=(1/TUniFreq[prev])
            TBigFreq[prev+"|"+ word]+=1
            prev=word
        else:
            i=1



#starts calculating the trigrams using the freqq of the bigrams
Ttri=nltk.FreqDist()
for s in sents[:100]:
    prevp=s["tags"][0]
    prevn=s["tags"][1]
    i=0
    for word in s["tags"]:
        if(i>1):
            Ttri[prevp+"|"+prevn+"|"+ word]+=(1/TBigFreq[prevp+"|"+prevn])
            prevp=prevn
            prevn=word
        else:
            i+=1

"""
print("---Trigrams")
for w in Ttri:
    print(w+"="+str(Ttri[w]))


print("BigTransitions of NOUN")
GetBigT('NOUN')
print("TriTransitions of NOUN|CONJ")
GetTriT('NOUN','DEF')
"""
print("EMISSION CALCUL")
i=0
emis={}
k=0
tagword=nltk.FreqDist()

for tag in Tuni.keys():
    k=k+1
   # print(Tuni.keys().__len__()-k)
    for word in words:
        N=0
        for s in sents[:100]:
            tags=s["tags"]
            tokens=s["tokens"]
            for i in range(0,tokens.__len__()):
                if(tokens[i]==word 
                and tags[i]==tag):
                    N+=1
        tagword[word+"|"+tag]=N/TUniFreq[tag]
k=0


"""
a=nltk.FreqDist()
import pickle
with open('emis', 'rb') as f:
   tagwordd = pickle.load(f)
k=0
N=0
for w in words:
    if("START" in w):
        print(w +"="+str(tagwordd[w]))
"""