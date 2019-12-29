from lxml import etree
import re
import nltk

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
    #s["tokens"][0:0] = ['<START>']
    s["tags"][0:2] = s["tags"][1:2]
    if len(s["tags"]) == len(s["tokens"]):
        s["len"] = len(s["tags"])
    else:
        print("LENGTH ERROR IN SENTENCE: ",s["num"])

# global counts 
mini_sents = sents[0:100]
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

# sets & lengths
word_set = set(all_words)
tag_set = set(all_tags)

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

# emission
def emission(t, w):
    return fd_emissions[(t,w)] / fd_tags[t]

def bi_transition(prev, t):
    if prev == '*':
        return fd_starts[t] / len(all_starts)
    elif t == 'STOP':
        return fd_ends[prev] / fd_tags[prev]
    else:
        return fd_bigrams[(prev,t)] / fd_tags[prev]

def tri_transition(prevprev, prev, t):
    if prev == '*':
        return fd_starts[t] / len(all_starts)
    elif prevprev == '*':
        return fd_starts_bigram[(prev,t)] / len(all_starts_bigram) 
    elif t == 'STOP':
        return fd_ends_bigram[(prevprev,prev)] / fd_bigrams[(prevprev,prev)]
    else:
        return fd_trigrams[(prevprev,prev,t)] / fd_bigrams[(prevprev,prev)]


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


















"""
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
"""



"""
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
"""

"""
# random test
import random
s = random.choice(sents)
print(s["num"])
for i in range(0,int(s["len"])):
    print(s["tokens"][i],"\t",s["tags"][i])
"""
