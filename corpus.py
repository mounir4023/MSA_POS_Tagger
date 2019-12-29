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

# removing the begining NULL
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
distinct_words = set(all_words)
distinct_tags = set(all_tags)
distinct_starts = set(all_starts)
distinct_ends = set(all_ends)

# unigrams: occurences = fd["tag"] / proba = fd.freq("tag")
tags_unigram = nltk.FreqDist(all_tags)



















"""
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
