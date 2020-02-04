from corpus import *
from hmm import *
from viterbi import *
import os
import re
import eel
import random
from os import listdir
from os.path import isfile, join
train_set=[]
lexicon=[]
model={}
mounted=0
print(mounted)
eel.init('GUI')
def tokenize( sentence ):
    
    os.chdir('api')
    source = open('source.txt','w',encoding='windows_1256')
    source.write(sentence)
    source.close()
    os.system('perl splitaffixfirstSol.pl < source.txt > output.txt')
    
    output = open('output.txt',encoding='windows_1256').read()
    output = re.sub(r'\s+',' ',output).split(' ')
    for w in output:
        if w == '':
            output.remove(w)
    
    os.chdir('..')
    
    return output


def tag ( sentence, model ):
    
    tokens = tokenize(sentence)
    s = { "len": len(tokens), "tokens":tokens, "raw": sentence }
    s["decoded"] = decode(s, model)
    return s



#### SPLITING AND MERGIN LEXICONS TEST ####
'''
split_factor = 4
split_lexicon("lexicons/lexicon.txt",split_factor)

lexicons_dir = "lexicons/"
l1 = lexicons_dir + "lexicon_part1.txt"
l2 = lexicons_dir + "lexicon_part2.txt"
#fuse_lexicons(l1,l2,lfusion)
l3 = lexicons_dir + "lexicon_part3.txt"
l4 = lexicons_dir + "lexicon_part4.txt"
lfusion = lexicons_dir + "fusion.txt"
fuse_n_lexicons( [l1,l2,l3,l4] , lfusion)


#### SPLITING AND MERGIN CORPORAS TEST ####

split_factor = 3
split_data("corporas/corpus.xml",split_factor)

corporas_dir = "corporas/"
c1 = corporas_dir + "corpus_part1.xml"
c2 = corporas_dir + "corpus_part2.xml"
#fuse_corporas(c1,c2,cfusion)
cfusion = corporas_dir + "fusion.xml"
c3 = corporas_dir + "corpus_part3.xml"
fuse_n_corporas( [c1,c2,c3], cfusion)

#### TEST THE FINAL FUSION ON TAGGING TASK ####
data = get_data(cfusion)
lexicon = get_lexicon(lfusion)
model = get_HMM(data,lexicon)

#print("tokenizing 'صباح الخير يا أصحاب'")
#print(tokenize('صباح الخير يا أصحاب'))
#print([ t for t in reversed(tag('صباح الخير يا أصحاب',model)) ] )
'''
@eel.expose()
def SplitCorpus(f,n):
    print(f,n)
    split_data("corporas/"+f,int(n))
    lc= listdir('corporas/') 
    ll= listdir('lexicons/') 
    
    eel.SendBack(lc,ll)
@eel.expose()
def SplitLexicon(f,n):
    print(f,n)
    split_lexicon("lexicons/"+f,int(n))
    lc= listdir('corporas/') 
    ll= listdir('lexicons/') 
    
    eel.SendBack(lc,ll)
@eel.expose()
def MergeCorporas(ll,lfusion):
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    
    for i in range(0,len(ll)):
        ll[i] = "corporas/"+ll[i]
    
    fuse_n_corporas( ll, "corporas/"+lfusion)
    lc= listdir('corporas/') 
    ll= listdir('corporas/') 
    eel.SendBack(lc,ll)
@eel.expose()
def MergeLexicons(ll,lfusion):
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    
    for i in range(0,len(ll)):
        ll[i] = "lexicons/"+ll[i]
    
    fuse_n_lexicons( ll, "lexicons/"+lfusion)
    lc= listdir('corporas/') 
    ll= listdir('lexicons/') 
    eel.SendBack(lc,ll)
@eel.expose()
def initt():
    '''
    global mounted
    global train_set
    global lexicon
    global model
    
    if(mounted==0):
        train_set = get_data("corporas/corpus.xml")[:]
        lexicon = get_lexicon("lexicons/lexicon.txt")
        model = get_HMM(train_set, lexicon)
        
    mounted=1
    eel.Notif("Loaded")
    res=[]
    tok=[]
    for ss in train_set[:50]:
        res+=ss["tags"]+['\n']
        tok+=ss["tokens"]
    print("here")
    eel.SendTrain(tok,res)
    print("done")
    '''
    lc= listdir('corporas/') 
    ll= listdir('lexicons/') 
    print(ll,lc)
    eel.SendBack(lc,ll)
@eel.expose()
def retrainmodel(l,c):
    global model
    print("zdzdz")
    train_set = get_data("corporas/"+c)
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    lexicon = get_lexicon("lexicons/"+l)
    model = get_HMM(train_set, lexicon)
    print("zdzdz")

@eel.expose()
def AddCorpus(e):
    
    global train_set
    global lexicon
    global model
    print("Importing corpus")
    f= open("corpuss.xml","w+",encoding="UTF-8")
    f.write(str(e))
    f.close()
    
    train_set+= get_data("corpuss.xml")[:]
    model = get_HMM(train_set, lexicon)
    
    print("done")
@eel.expose()
def AddLexicon(e):
    
    global train_set
    global lexicon
    global model
    print("Importing Lexicon")
    f= open("lexiconn.txt","w+",encoding="UTF-8")
    f.write(str(e))
    f.close()
    
    lexicon.update( get_lexicon("lexiconn.txt"))
    model = get_HMM(train_set, lexicon)

    print("done")
@eel.expose()
def GetLexiconContent(f):
    print(f)
    eel.SetLexiconContent(''.join(open('lexicons/'+f,encoding='UTF-8').readlines()[:100]))
@eel.expose()
def GetCorpusContent(f):
    print(f)
    eel.SetCorpusContent(''.join(open('corporas/'+f,encoding='UTF-8').readlines()[:100]))

@eel.expose()
def DeleteCorpus(f):
    os.remove('corporas/'+f )
    lc= listdir('corporas/') 
    ll= listdir('lexicons/') 
    
    eel.SendBack(lc,ll)
@eel.expose()
def DeleteLexicon(f):
    os.remove('lexicons/'+f )
    lc= listdir('corporas/') 
    ll= listdir('lexicons/') 
    
    eel.SendBack(lc,ll)
@eel.expose()
def TagText(text):

    
    ch=nltk.sent_tokenize(text)
    #print("tokenizing "+ch)
    res=[]
    tok=[]
    output=''
    
    for ss in ch:
        s=tokenize(ss)
        print(s)
    #s = random.choice(train_set)
        s = {'num':00,'len':len(s),'raw':text,'tokens':tokenize(text),'tags':[]}
        print("phrase: ",s["num"])
        s["decoded"] = decode(s, model)
        res+=s["decoded"]
        tok+=s["tokens"]
        
    print(tok)
    print(res)
    
    eel.SendRes(tok,res)
""" 

        eel.SendRes(s["tokens"],s["decoded"])
   for i in range(0,s["len"]):
        if s["tokens"][i] in model["forget_words"]:
            print("*UNK*\t",s["tokens"][i],"\t",s["tags"][i],"\t",s["decoded"][i])
        else:
            print("     \t",s["tokens"][i],"\t",s["tags"][i],"\t",s["decoded"][i])
"""

    

eel.start('UIMaterialize.html',mode='chrome',size=(500,500))
