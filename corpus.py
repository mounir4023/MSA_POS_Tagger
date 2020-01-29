from lxml import etree
import random
import re
import nltk
import os
import math


############ CORPUS ############

#read data into dict
def get_data( path ):
    
    # init
    root = etree.parse(path)
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

# split corpus file into n parts files
def split_data ( path , n ):
    
    #data = random.shuffle(get_data(path))
    data = get_data(path)
    size = math.floor( len(data) / n )
    
    for i in range(0,n):
        start = i*(size)
        end = (i+1)*size
        if i == n-1:
            sents = data[start:]
        else:
            sents = data[start:end]
        name = re.sub(".xml","_part"+str(i+1)+".xml",path)
        content = "<?xml version='1.0' encoding='utf-8'?>\n<CORPUS>\n"
        for sent in sents:
            content +="<Phrase>\n"
            content +="<Num_phrase>"+sent["num"]+"</Num_phrase>\n"
            content +="<Text>"+sent["raw"]+"</Text>\n"
            content +="<Tokenisation>"+" ".join(sent["tokens"])+"</Tokenisation>\n"
            content +="<POS_Tag>NULL "+" ".join(sent["tags"])+"\n</POS_Tag>\n"
            content +="<Nb_Mot>"+str(len(sent["tokens"][1:]))+"</Nb_Mot>\n"
            content +="<Nb_Token>"+str(len(sent["tags"][1:]))+"</Nb_Token>\n"
            content +="</Phrase>\n"
        content += "</CORPUS>"
        f = open(name,"w")
        f.write(content)
        f.close()

# merge 2 corporas into one new file
def fuse_corporas( c1 , c2, name ):
    
    corpus1 = get_data(c1)
    corpus2 = get_data(c2)
    
    sents = [ sent["raw"] for sent in corpus1 ]
    for sent in corpus2:
        if sent["raw"] not in sents:
            corpus1.append(sent)
            
    fusion = sorted(corpus1, key = lambda sent : int(sent["num"]))
            
    content = "<?xml version='1.0' encoding='utf-8'?>\n<CORPUS>\n"
    for sent in fusion:
        content += "<Phrase>\n"
        content +="<Num_phrase>"+sent["num"]+"</Num_phrase>\n"
        content +="<Text>"+sent["raw"]+"</Text>\n"
        content +="<Tokenisation>"+" ".join(sent["tokens"])+"</Tokenisation>\n"
        content +="<POS_Tag>NULL "+" ".join(sent["tags"])+"\n</POS_Tag>\n"
        content +="<Nb_Mot>"+str(len(sent["tokens"][1:]))+"</Nb_Mot>\n"
        content +="<Nb_Token>"+str(len(sent["tags"][1:]))+"</Nb_Token>\n"
        content +="</Phrase>\n"
    content += "</CORPUS>"
    f = open(name,"w")
    f.write(content)
    f.close()
    
    print("\n\n Corporas fusion: \n")
    print("size of corpus1 :", os.path.getsize(c1))
    print("size of corpus2 :", os.path.getsize(c2))
    print("size of fusion   :", os.path.getsize(name))
    
    return os.path.getsize(c1), os.path.getsize(c2), os.path.getsize(name)
    
# merge n corporas into one new file
def fuse_n_corporas( corporas, name ):
    
    if len(corporas) <= 1:
        return

    fuse_corporas(corporas[0],corporas[1],name)    
    for c in corporas[2:]:
        fuse_corporas(c,name,name)



    

############ LEXICON ############

# read lexicon into dict
def get_lexicon( path ):
    
    lexicon = { }
    lines = open(path).readlines()
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

# split lexicon file into n parts files
def split_lexicon( path , n ):
    
    lexicon = get_lexicon(path)
    keys = [k for k in lexicon.keys()]
    random.shuffle(keys)
    size = math.floor( len(lexicon) / n )
    
    for i in range(0,n):
        start = i*(size)
        end = (i+1)*size
        if i == n-1:
            k = keys[start:]
        else :
            k = keys[start:end]
        l = { } 
        for key in k:
            l[key] = lexicon[key]
        name = re.sub(".txt","_part"+str(i+1)+".txt",path)
        content = ""
        for item in l.items():
            content += item[0]+" "
            for t in item[1]:
                content += t+" "
            content +="\n"
        f = open(name,"w")
        f.write(content)
        f.close()
        
# merge 2 lexicons into one new file
def fuse_lexicons( l1 , l2, name ):
    
    # read the first lexicon
    lexicon1 = { }
    lines = open(l1).readlines()
    for l in lines:
        l = re.sub(r'\s+',' ',l)
        l = l.split(' ')
        for t in l:
            if t == '':
                l.remove(t)
        lexicon1[l[0]] = [ ]
        for t in l[1:]:
            lexicon1[l[0]].append(t)
            
    # read the second lexicon
    lexicon2 = { }
    lines = open(l2).readlines()
    for l in lines:
        l = re.sub(r'\s+',' ',l)
        l = l.split(' ')
        for t in l:
            if t == '':
                l.remove(t)
        lexicon2[l[0]] = [ ]
        for t in l[1:]:
            lexicon2[l[0]].append(t)
            
    # merge the two lexicons
    fusion = { }
    for item in lexicon1.items():
        fusion[item[0]] = [ t for t in item[1] ]

    for item in lexicon2.items():
        
        if not item[0] in fusion.keys():
            fusion[item[0]] = [ t for t in item[1] ]
        
        else:
            tmp = [ t for t in fusion[item[0]] ]
            for t in item[1]:
                if not t in tmp:
                    tmp.append(t)
            fusion[item[0]] = tmp
            
    # save fusion lexicon to file
    content = ""
    for item in fusion.items():
        content += item[0]+" "
        for t in item[1]:
            content += t+" "
        content +="\n"
    f = open(name,"w")
    f.write(content)
    f.close()
    
    """
    print("\n\n Lexicons fusion: \n")
    print("size of lexicon1 :", os.path.getsize(l1))
    print("size of lexicon2 :", os.path.getsize(l2))
    print("size of fusion   :", os.path.getsize(name))
    
    print("lines of lexicon1 :", len(lexicon1) )
    print("lines of lexicon2 :", len(lexicon2) )
    print("lines of fusion   :", len(fusion) )
    """
    
    return os.path.getsize(l1), os.path.getsize(l2), os.path.getsize(name)
        
        
# merge 2 lexicons into one new file
def fuse_n_lexicons( lexicons, name ):
    
    f = open(name,"w")
    f.write("")
    f.close()
    
    for l in lexicons:
        fuse_lexicons(l,name,name)








