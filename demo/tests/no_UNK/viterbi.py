from lxml import etree
import random
import re
import nltk


def possible_tags(k ,s , model):
    if k == -1 or k == -2:
        return ['*']
    else: 
        #return pos_lexicon[w]
        #return model["all_tags"]
        w = s["tokens"][k]
        if w in model["lexicon_words"]:
            return model["lexicon"][w]
        else:
            return model["all_tags"]

def viterbi_transition(prevprev, prev, t , model):
    try:
        #return model["smooth_transition"][(prevprev,prev,t)]
        return model["tri_transition"][(prevprev,prev,t)]
    except:
        return 0

def viterbi_emission(t, w, model):
    try:
        if w in model["corpus_words"]:
            return model["emission"][(t,w)]
        else:
            #return model["emission"][(t,'UNK')]
            return 1
    except:
        return 0
    
def decode(s, model):

    #init 
    pi = { (-1,'*','*'): 1 }
    bp = { }
    n = s["len"]-1
    decoded = ['*' for i in range(0,s["len"]) ]

    # decoding
    for i in range(0,s["len"]):

        for u in possible_tags(i, s, model):
            for v in possible_tags(i-1, s, model):

                w = possible_tags(i-2, s, model)[0]
                pi[ (i,v,u) ] = pi [ (i-1,w,v) ] * viterbi_transition(w,v,u,model) * viterbi_emission(u,s["tokens"][i],model)
                bp[ (i,v,u) ] = w

                for w in possible_tags(i-2, s, model)[1:]:
                    tmp = pi [ (i-1,w,v) ] * viterbi_transition(w,v,u,model) * viterbi_emission(u,s["tokens"][i],model)
                    if tmp > pi [ (i,v,u) ] :
                        pi[ (i,v,u) ] = tmp
                        bp[ (i,v,u) ] = w

    # Yn Yn-1 
    u = possible_tags(n, s, model)[0]
    v = possible_tags(n-1, s, model)[0]
    max_uv_end = pi[ (n,v,u) ] * viterbi_transition(v,u,'STOP',model)
    decoded[n] = u
    if n>0:
        decoded[n-1] = v
    for u in possible_tags(n, s, model):
        for v in possible_tags(n-1, s, model):
            tmp = pi[ (n,v,u) ] * viterbi_transition(v,u,'STOP',model)
            if tmp > max_uv_end:
                max_uv_end = tmp
                decoded[n] = u
                if n>0:
                    decoded[n-1] = v

    # Y0 Y1 .... Yn-2
    for k in reversed(range(0,n-2+1)):
        decoded[k] = bp [ (k+2, decoded[k+1], decoded[k+2] ) ]

    return decoded
         
