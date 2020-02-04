from lxml import etree
import random
import re
import nltk


######################## DATA ##########################

# reading corpus from xml
root = etree.parse("corpus.xml")
sents = [ ]

# xml to dict for each sentence 
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

# cleaning empty tokens and tags
for s in sents:
    for t in s["tokens"]:
        if t == '' or t == ' ':
            s["tokens"].remove(t)
    for t in s["tags"]:
        if t == '' or t == ' ':
            s["tags"].remove(t)

# removing the begining NULL tag
for s in sents:
    s["tags"][0:2] = s["tags"][1:2]
    if len(s["tags"]) == len(s["tokens"]):
        s["len"] = len(s["tags"])
    else:
        print("LENGTH ERROR IN SENTENCE: ",s["num"])

# global counts 
#mini_sents = [ random.choice(sents) for i in range(0,200) ]
mini_sents = sents[:200]
all_words = [ ]
all_emissions = [ ]
all_tags = [ ]
all_bigrams = [ ]
all_trigrams = [ ]
all_starts = [ ]
all_ends = [ ]
all_starts_bigram = [ ]
all_ends_bigram = [ ]
for s in mini_sents:
    for i in range(0,s["len"]):
        w = s["tokens"][i]
        t = s["tags"][i]
        all_words.append( w )
        all_emissions.append( (t,w) )
        all_tags.append( t )
        if i>0:
            prev = s["tags"][i-1]
            all_bigrams.append( (prev,t) )
            if i>1:
                prevprev = s["tags"][i-2]
                all_trigrams.append( (prevprev,prev,t) )
    all_starts.append(s["tags"][0])
    all_ends.append(s["tags"][-1])
    all_starts_bigram.append( (s["tags"][0],s["tags"][1]) )
    all_ends_bigram.append( (s["tags"][-2],s["tags"][-1]) )

# sets lengths
word_set = set(all_words)
tag_set = set(all_tags)
corpus_size = len(all_starts)

# freq dists
fd_words = nltk.FreqDist(all_words)
fd_emissions = nltk.FreqDist(all_emissions)
fd_tags = nltk.FreqDist(all_tags)
fd_bigrams = nltk.FreqDist(all_bigrams)
fd_trigrams = nltk.FreqDist(all_trigrams)
fd_starts = nltk.FreqDist(all_starts)
fd_ends = nltk.FreqDist(all_ends)
fd_starts_bigram = nltk.FreqDist(all_starts_bigram)
fd_ends_bigram = nltk.FreqDist(all_ends_bigram)

######################  HMM  ##########################

def emission(t, w):
    return fd_emissions[(t,w)] / fd_tags[t]

def uni_transition(t):
    return fd_words.freq(t)

def bi_transition(prev, t):
    if prev == '*':
        return fd_starts[t] / corpus_size
    elif t == 'STOP':
        return fd_ends[prev] / fd_tags[prev]
    else:
        return fd_bigrams[(prev,t)] / fd_tags[prev]

def tri_transition(prevprev, prev, t):
    if prev == '*':
        return fd_starts[t] / corpus_size
    elif prevprev == '*':
        return fd_starts_bigram[(prev,t)] / corpus_size
    elif t == 'STOP':
        if fd_ends_bigram[(prevprev,prev)] == 0:
            return 0
        return fd_ends_bigram[(prevprev,prev)] / fd_bigrams[(prevprev,prev)]
    else:
        if fd_trigrams[(prevprev,prev,t)] == 0:
            return 0
        return fd_trigrams[(prevprev,prev,t)] / fd_bigrams[(prevprev,prev)]


######################  Viterbi ##########################

def possible_tags(k):
    if k == -1 or k == -2:
        return ['*']
    else: 
        return list(set(all_tags))

# init
#s = random.choice(mini_sents)
s = sents[4023]
pi = { (-1,'*','*'): 1 }
bp = { }
n = s["len"]-1
decoded = ['*' for i in range(0,s["len"]) ]

# decoding
for i in range(0,s["len"]):
    print("Position ",i," /",n)

    for u in possible_tags(i):
        for v in possible_tags(i-1):

            w = possible_tags(i-2)[0]
            pi[ (i,v,u) ] = pi [ (i-1,w,v) ] * tri_transition(w,v,u) * emission(u,s["tokens"][i])
            bp[ (i,v,u) ] = w

            for w in possible_tags(i-2)[1:]:
                tmp = pi [ (i-1,w,v) ] * tri_transition(w,v,u) * emission(u,s["tokens"][i])
                if tmp > pi [ (i,v,u) ] :
                    pi[ (i,v,u) ] = tmp
                    bp[ (i,v,u) ] = w

# Yn Yn-1 then Yi 0..n-2
u = possible_tags(n)[0]
v = possible_tags(n-1)[0]
max_uv_end = pi[ (n,v,u) ] * tri_transition(v,u,'STOP')
decoded[n] = u
if n>0:
    decoded[n-1] = v

for u in possible_tags(n):
    for v in possible_tags(n-1):
        tmp = pi[ (n,v,u) ] * tri_transition(v,u,'STOP')
        if tmp > max_uv_end:
            max_uv_end = tmp
            decoded[n] = u
            if n>0:
                decoded[n-1] = v


# final test
print(n," ",s["tokens"][n]," ",s["tags"][n]," ",decoded[n])
for k in reversed(range(0,n-2+1)):
    print(k+1," ",s["tokens"][k+1]," ",s["tags"][k+1]," ",decoded[k+1])
    decoded[k] = bp [ (k+2, decoded[k+1], decoded[k+2] ) ]
        















"""
    #max_uv_end = random.uniform(0,0.001) * random.uniform(1,10)


for s in sents[:10]:
 p = tri_transition( '*','*',s["tags"][0] ) * emission( s["tags"][0] , s["tokens"][0] ) 
 p = p *  tri_transition( '*',s["tags"][0],s["tags"][1] ) * emission( s["tags"][1] , s["tokens"][1] ) 

 for i in range(2,s["len"]):
     p = p * tri_transition(s["tags"][i-2],s["tags"][i-1],s["tags"][i]) * emission( s["tags"][i], s["tokens"][i] ) 

 p = p * tri_transition(s["tags"][-2],s["tags"][-1],'STOP')
 print(p)

"""


"""
print([item for item in pi.items() if item[1] >0])
print([item for item in bp.items() if item[1] == '*' ])
"""

"""
# final test
print(n," ",s["tokens"][n]," ",s["tags"][n]," ",decoded[n])
for k in reversed(range(0,n-2+1)):
    print(k+1," ",s["tokens"][k+1]," ",s["tags"][k+1]," ",decoded[k+1])
    decoded[k] = bp [ (k+2, decoded[k+1], decoded[k+2] ) ]
        

print(" ")
print(decoded)
"""













"""
#for i in range(0,s["len"]):
#    print("token ",s["tokens"][i]," original ",s["tags"][i], " predicted ",decoded[i])



for t in list(tag_set):
    try:
        print(tri_transition(t,'PUNC','STOP'))
        print(t)
    except:
        pass
print(list(tag_set))
#some 1.0 s and the others were caught in except > all is good


print(tri_transition('SUFF_F_S_GTIV','PUNC','STOP'))
#1

s = sents[10]
tags = s["tags"]
tokens = s["tokens"]

for i in range(0,s["len"]):
    #print("w|t ",emission(tags[i],tokens[i]))
    print("\n position: ",i)
    print("emission: ",emission(tags[i],tokens[i]))

print(" ")
print("start tag: ",bi_transition('*',tags[0]))
print("start tag2: ",tri_transition('*','*',tags[0]))
print("start bigram: ",tri_transition('*',tags[0],tags[1]))
print("end tag: ",bi_transition(tags[-1],'STOP'))
print("end bigram: ",tri_transition(tags[-2],tags[-1],'STOP'))
print("sample end bigram: ",tags[-2]," ",tags[-1]," ",fd_ends_bigram[(tags[-2],tags[-1])])
print("sample end bigram all occurences: ",fd_bigrams[(tags[-2],tags[-1])])


s = sents[0]
tags = s["tags"]
tokens = s["tokens"]

for i in range(0,s["len"]):
    print("w|t ",emission(tags[i],tokens[i]))

# all > 0 correct

for t in list(tag_set):
    try:
        print(tri_transition(t,'PUNC','STOP'))
        print(t)
    except:
        pass
#some 0 s only

print(tri_transition('CONJ','NN','PUNC'))
# N / 0 exception
print(tri_transition('CONJ','DEF','NN'))
#0.00
print(tri_transition('*','*','DEF'))
#0.07
print(tri_transition('*','*','CONJ'))
#0.02
print(bi_transition('*','CONJ'))
#0.02
print(bi_transition('*','DEF'))
#0.07
print(bi_transition('PUNC','STOP'))
1.
print(emission('DEF','ال'))
0.96
print(emission('PUNC','.'))
1.


distinct_words = set(all_words)
distinct_tags = set(all_tags)
distinct_starts = set(all_starts)
distinct_ends = set(all_ends)
#print(tags_unigram.freq("NOUN"))
for t in list(distinct_tags)[:10]:
    print("occurences: ", tags_unigram[t]," / ",len(all_words))
    print("probability: ", tags_unigram.freq(t))
    print(tags_unigram[t]/len(all_words) == tags_unigram.freq(t))

print(tags_unigram.N() == len(all_words) )



# random test
import random
s = random.choice(sents)
print(s["num"])
for i in range(0,int(s["len"])):
    print(s["tokens"][i],"\t",s["tags"][i])
"""







