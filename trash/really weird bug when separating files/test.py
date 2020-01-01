from corpus import get_data #,get_lexicon
from hmm import get_HMM
from viterbi import decode
import random

# test
#train_set = [ random.choice(sents) for i in range(0,200) ]
train_set = get_data("corpus.xml")[:200]
model = get_HMM(train_set)

s = random.choice(train_set)
#s = sents[4023]
print("phrase: ",s["num"])
s["decoded"] = decode(s, model)
for i in range(0,s["len"]):
    if s["tokens"][i] in forget_words:
        print("*UNK*\t",s["tokens"][i],"\t",s["tags"][i],"\t",s["decoded"][i])
    else:
        print("     \t",s["tokens"][i],"\t",s["tags"][i],"\t",s["decoded"][i])
 
