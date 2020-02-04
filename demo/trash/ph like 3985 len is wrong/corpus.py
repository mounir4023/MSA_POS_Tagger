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


# random test
import random
s = random.choice(sents)
s = sents[3895]
print(s["num"])
print(s["len"])
for i in range(0,int(s["len"])):
    print(s["tokens"][i],"\t",s["tags"][i])
