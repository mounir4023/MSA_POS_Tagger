from lxml import etree
import re
import nltk
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

for s in root.xpath("/CORPUS/Phrase"):
    tokens = re.sub(r'\s+',' ',s[2].text)
    
    sents.append({
            'num':s[0].text,
            'raw':s[1].text,
            'tokens':tokens.split(" "),
            'tags':s[3].text,
        })
NU=0
for s in sents:
    for t in s["tokens"]:
        
        if t == '' or t == ' ':
            s["tokens"].remove(t)
        else:
            NU+=1

matUni=nltk.FreqDist()
UniFreq=nltk.FreqDist()
for s in sents[:20]:

    for word in s["tokens"]:
        matUni[word]+=(1/NU)
        UniFreq[word]+=1

NB=0
MatBig=nltk.FreqDist()
BigFreq=nltk.FreqDist()
for s in sents[:20]:
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
for s in sents[:20]:
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
for s in sents[:20]:

    for word in s["tags"].split(" "):
        Tuni[word]+=(1/NU)
        TUniFreq[word]+=1

NB=0
Tbig=nltk.FreqDist()
TBigFreq=nltk.FreqDist()
for s in sents[:20]:
    prev=s["tags"].split(" ")[0]
    i=0
    for word in s["tags"].split(" "):
        if(i!=0):
            Tbig[prev+"|"+ word]+=(1/TUniFreq[prev])
            TBigFreq[prev+"|"+ word]+=1
            prev=word
        else:
            i=1



#starts calculating the trigrams using the freqq of the bigrams
Ttri=nltk.FreqDist()
for s in sents[:20]:
    prevp=s["tags"].split(" ")[0]
    prevn=s["tags"].split(" ")[1]
    i=0
    for word in s["tags"].split(" "):
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
"""
print("BigTransitions of NOUN")
GetBigT('NOUN')
print("TriTransitions of NOUN|CONJ")
GetTriT('NOUN','CONJ')