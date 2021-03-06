from lxml import etree
import random
import re
import nltk


##### preparing data into dict

def get_data( path ):
    
    # init
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
            
    return sents


##### preparing lexicon into dict

def get_lexicon( path ):
    
    lexicon = { }
    lines = open("lexicon.txt").readlines()
    for l in lines:
        l = re.sub(r'\s+',' ',l)
        l = l.split(' ')
        for t in l:
            if t == '':
                l.remove(t)
        lexicon[l[0]] = [ ]
        for t in l[1:]:
            lexicon[l[0]].append(t)
            
    return lexicon









