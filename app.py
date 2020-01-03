from corpus import *
from hmm import *
from viterbi import *
import os
import re
import random

def retrain_model( dir ):
    #for file in dir: create one corpus file having containing them all
    #get_data (that new file)
    return
    
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
    
    token = tokenize(sentence)
    s = { "len": len(tokens), "tokens":tokens, "raw": sentence }
    s["decoded"] = decode(s, model)
    return s

print("tokenizing 'صباح الخير يا أصحاب'")
print(tokenize('صباح الخير يا أصحاب'))
