from lxml import etree
import random
import re
import nltk


##### training an HMM on data

def get_HMM( train_set , lexicon ):
    
    # define formulas

    def emission(t, w):
        return fd_emissions[(t,w)] / fd_tags[t]

    def uni_transition(t):
        return fd_words.freq(t)

    def bi_transition(prev, t):
        if prev == '*':
            return fd_starts[t] / corpus_size
        elif t == 'STOP':
            return fd_ends[prev] / fd_tags[prev]
        else:
            return fd_bigrams[(prev,t)] / fd_tags[prev]

    def tri_transition(prevprev, prev, t):
        if prev == '*':
            return fd_starts[t] / corpus_size
        elif prevprev == '*':
            return fd_starts_bigram[(prev,t)] / corpus_size
        elif t == 'STOP':
            if fd_ends_bigram[(prevprev,prev)] == 0:
                return 0
            return fd_ends_bigram[(prevprev,prev)] / fd_bigrams[(prevprev,prev)]
        else:
            if fd_trigrams[(prevprev,prev,t)] == 0:
                return 0
            return fd_trigrams[(prevprev,prev,t)] / fd_bigrams[(prevprev,prev)]

    def smooth_transition(prevprev, prev, t):
        return 0.01 + 0.09 * uni_transition(t) + 0.2 * bi_transition(prev,t) + 0.7 * tri_transition(prevprev,prev,t)
    

    """
    # UNK, forgetting rare words
    all_words = [ ]
    forget_words = [ ]

    for s in train_set:
        for w in s["tokens"]:
            all_words.append(w)
    fd_words = nltk.FreqDist(all_words)

    for item in fd_words.items():
        if item[1]<2:
            forget_words.append(item[0])
    """
    forget_words = [ ]

    # counting
    all_words = [ ]
    all_emissions = [ ]
    all_tags = [ ]
    all_bigrams = [ ]
    all_trigrams = [ ]
    all_starts = [ ]
    all_ends = [ ]
    all_starts_bigram = [ ]
    all_ends_bigram = [ ]
    for s in train_set:
        for i in range(0,s["len"]):
            w = s["tokens"][i]
            if w in forget_words:
                w = 'UNK'
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

    # sets, lengths
    word_set = set(all_words)
    tag_set = set(all_tags)
    corpus_size = len(all_starts)

    # freq dists
    fd_words = nltk.FreqDist(all_words)
    fd_emissions = nltk.FreqDist(all_emissions)
    fd_tags = nltk.FreqDist(all_tags)
    fd_bigrams = nltk.FreqDist(all_bigrams)
    fd_trigrams = nltk.FreqDist(all_trigrams)
    fd_starts = nltk.FreqDist(all_starts)
    fd_ends = nltk.FreqDist(all_ends)
    fd_starts_bigram = nltk.FreqDist(all_starts_bigram)
    fd_ends_bigram = nltk.FreqDist(all_ends_bigram)
    
    # training
    model = {
        "emission": {},
        "uni_transition": {},
        "bi_transition": {},
        "tri_transition": {},
        "smooth_transition": {},

        "forget_words": [ w for w in forget_words ],
        "corpus_words": all_words,
        "lexicon": lexicon,
        "lexicon_words": [ w for w in lexicon.keys() ],
        "all_tags": list(set( [ t for item in lexicon.items() for t in item[1] ] )),
    }

    for w in fd_words.keys():
        for t in fd_tags.keys():
            model["emission"][(t,w)] = emission(t,w)
            model["uni_transition"][t] = uni_transition(t)

    dest = [ t for t in fd_tags.keys() ]
    dest.append('STOP')
    source = [ t for t in fd_tags.keys() ]
    source.append('*')

    for t in dest:
        for prev in source:
            model["bi_transition"][(prev,t)] = bi_transition(prev,t)

    for t in dest:
        for prev in source:
            for prevprev in source:
                model["tri_transition"][(prevprev,prev,t)] = tri_transition(prevprev,prev,t)
                model["smooth_transition"][(prevprev,prev,t)] = smooth_transition(prevprev,prev,t)
    
    return model

