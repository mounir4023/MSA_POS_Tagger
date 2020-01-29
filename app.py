from corpus import *
from hmm import *
from viterbi import *
import os
import re
import random


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

split_factor = 2
split_data("corporas/corpus.xml",split_factor)

corporas_dir = "corporas/"
c1 = corporas_dir + "corpus_part1.xml"
c2 = corporas_dir + "corpus_part2.xml"
cfusion = corporas_dir + "fusion.xml"
fuse_corporas(c1,c2,cfusion)

#### TEST THE FINAL FUSION ON TAGGING TASK ####
data = get_data(cfusion)
lexicon = get_lexicon(lfusion)
model = get_HMM(data,lexicon)

#print("tokenizing 'صباح الخير يا أصحاب'")
#print(tokenize('صباح الخير يا أصحاب'))
#print([ t for t in reversed(tag('صباح الخير يا أصحاب',model)) ] )
