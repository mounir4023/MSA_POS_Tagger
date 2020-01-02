from corpus import get_data ,get_lexicon
from hmm import get_HMM
from viterbi import decode
from evaluation import eval_model
import random
import csv

data = random.shuffle(get_data("corpus.xml"))
train_set = get_data("corpus.xml")[:3000]
test_set = get_data("corpus.xml")[3000:]
lexicon = get_lexicon("lexicon.txt")
model = get_HMM(train_set, lexicon)

results = eval_model(train_set[:1500], model)

conditions = results["worst_tags"][:10]
samples = results["worst_codes"][:10]
print(results["confusion"].tabulate( conditions, samples ) )

"""
import pandas as pd
tmp = pd.DataFrame(results["confusion"]).fillna(0)
#print(results["confusion"].items())
print(tmp)
"""

"""
print("train set: 3000")
print("sent acc: ",results["sent_accuracy"])
print("     acc: ",results["accuracy"])

results = eval_model(test_set, model)

print("test set: 1000")
print("sent acc: ",results["sent_accuracy"])
print("     acc: ",results["accuracy"])

"""

"""
#print("\nworst_tags\n",results["worst_tags"])
#print("\nworst_words:\n",results["worst_words"])
#print("confusion matrix:")
#print(results["confusion"].tabulate())
"""
