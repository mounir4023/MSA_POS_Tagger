from lxml import etree
import random
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
    s["tags"][0:2] = s["tags"][1:2]
    if len(s["tags"]) == len(s["tokens"]):
        s["len"] = len(s["tags"])
    else:
        print("LENGTH ERROR IN SENTENCE: ",s["num"])

# corpus based lexicon
corpus_lex = { }
tested_words = [ ]
for s in sents:
    for i in range(0,s["len"]):
        w = s["tokens"][i]
        t = s["tags"][i]
        if w in tested_words:
            if t not in corpus_lex[w]:
                corpus_lex[w].append(t)
        else:
            tested_words.append(w)
            corpus_lex[w] = [t]

# export corpus lexicon
content = ""
for item in corpus_lex.items():
    content += item[0]+" "
    for t in item[1]:
        content += t+" "
    content +="\n"
f = open("corpus_lexicon.txt","w")
f.write(content)
f.close()

# SAIE based lexicon
saie_lex = { }
lines = open("poor_lexicon.txt").readlines()
for l in lines:
    l = re.sub(r'\s+',' ',l)
    l = l.split(' ')
    for t in l:
        if t == '':
            l.remove(t)
    saie_lex[l[0]] = [ ]
    for t in l[1:]:
        saie_lex[l[0]].append(t)


# merge the two lexicons
lexicon = { }
for item in saie_lex.items():
    lexicon[item[0]] = [ t for t in item[1] ]

for item in corpus_lex.items():
    
    if not item[0] in lexicon.keys():
        lexicon[item[0]] = [ t for t in item[1] ]
    
    else:
        tmp = [ t for t in lexicon[item[0]] ]
        for t in item[1]:
            if not t in tmp:
                tmp.append(t)
        lexicon[item[0]] = tmp

# export rich lexicon
content = ""
for item in lexicon.items():
    content += item[0]+" "
    for t in item[1]:
        content += t+" "
    content +="\n"
f = open("rich_lexicon.txt","w")
f.write(content)
f.close()


# comparing between lexicons
words = 0
tags = 0
for item in corpus_lex.items():
    words += 1
    for t in item[1]:
        tags +=1
print("Corpus lexicon\twords: ",words,"\ttags: ",tags)

words = 0
tags = 0
for item in saie_lex.items():
    words += 1
    for t in item[1]:
        tags +=1
print("  saie lexicon\twords: ",words,"\ttags: ",tags)

words = 0
tags = 0
for item in lexicon.items():
    words += 1
    for t in item[1]:
        tags +=1
print("  rich lexicon\twords: ",words,"\ttags: ",tags)












"""
for item in saie_lex.items():
    if item[1][-1] == '':
        print(item)
        """



"""
for item in corpus_lex.items():
    if len(item[1])>1:
        print(item)
"""








"""
# forgetting rare words
#sents = [ random.choice(sents) for i in range(0,200) ]
sents = sents[:200]
all_words = [ ]
forget_words = [ ]

for s in sents:
    for w in s["tokens"]:
        all_words.append(w)
fd_words = nltk.FreqDist(all_words)

for item in fd_words.items():
    if item[1]<2:
        forget_words.append(item[0])


# counts 
all_words = [ ]
all_emissions = [ ]
all_tags = [ ]
all_bigrams = [ ]
all_trigrams = [ ]
all_starts = [ ]
all_ends = [ ]
all_starts_bigram = [ ]
all_ends_bigram = [ ]
for s in sents:
    for i in range(0,s["len"]):
        w = s["tokens"][i]
        if w in forget_words:
            w = 'UNK'
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

def smooth_transition(prevprev, prev, t):
    return 0.01 + 0.09 * uni_transition(t) + 0.2 * bi_transition(prev,t) + 0.7 * tri_transition(prevprev,prev,t)

# add 
def smooth_emission(t,w):
    if w in forget_words:
        #return 1
        return emission(t, 'UNK')
    else:
        return emission(t,w)


######################  Viterbi ##########################

def possible_tags(k, w):
    if k == -1 or k == -2:
        return ['*']
    else: 
        #return pos_lexicon[w]
        return list(set(all_tags))

#s = random.choice(sents)
def viterbi(s):

    #init 
    pi = { (-1,'*','*'): 1 }
    bp = { }
    n = s["len"]-1
    decoded = ['*' for i in range(0,s["len"]) ]

    # decoding
    for i in range(0,s["len"]):

        for u in possible_tags(i):
            for v in possible_tags(i-1):

                w = possible_tags(i-2)[0]
                pi[ (i,v,u) ] = pi [ (i-1,w,v) ] * tri_transition(w,v,u) * smooth_emission(u,s["tokens"][i])
                bp[ (i,v,u) ] = w

                for w in possible_tags(i-2)[1:]:
                    tmp = pi [ (i-1,w,v) ] * tri_transition(w,v,u) * smooth_emission(u,s["tokens"][i])
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

    for k in reversed(range(0,n-2+1)):
        decoded[k] = bp [ (k+2, decoded[k+1], decoded[k+2] ) ]

    return decoded
        

# test
s = random.choice(sents)
s["decoded"] = viterbi(s)
print("phrase: ",s["num"])
for i in range(0,s["len"]):
    if s["tokens"][i] in forget_words:
        print(s["tokens"][i],"\t",s["tags"][i],"\t",s["decoded"][i],"\t*UNK Word*")
    else:
        print(s["tokens"][i],"\t",s["tags"][i],"\t",s["decoded"][i])

"""
