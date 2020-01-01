from lxml import etree
import random
import re
import nltk


######################## DATA ##########################

# reading corpus from xml
root = etree.parse("MSA_POS_Tagger/corpus.xml")
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
#mini_sents = [ random.choice(sents) for i in range(0,1000) ]
mini_sents = sents[:]
all_tags = [ ]
for s in mini_sents:
    for i in range(0,s["len"]):
        t = s["tags"][i]
        all_tags.append( t )

# sets lengths
tag_set = set(all_tags)


# freq dists
fd_tags = nltk.FreqDist(all_tags)


print ([a_tag for a_tag in fd_tags if (fd_tags[a_tag]==1)])

### wlh mafhemt lol xD m3a lewel banouli kyn klk tag erroné
### el mouhim el moucharaka lol



