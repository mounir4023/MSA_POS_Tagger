from lxml import etree
import re


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

# adding the START state
for s in sents:
    #s["tokens"][0:0] = ['<START>']
    s["tags"][0:2] = s["tags"][1:2]


# global counts 
mini_sents = sents[0:100]
all_words = [ ]
all_tags = [ ]
for s in mini_sents:
    for w in s["tokens"]:
        all_words.append(w)
    for t in s["tags"]:
        all_tags.append(t)

print(len(all_words))
print(len(all_tags))
distinct_words = set(all_words)
distinct_tags = set(all_tags)
print(len(distinct_words))
print(len(distinct_tags))




















"""
# random test
import random
s = random.choice(sents)
print(s["num"])
for i in range(0,int(s["len"])):
    print(s["tokens"][i],"\t",s["tags"][i])
"""
