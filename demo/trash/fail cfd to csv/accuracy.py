from corpus import get_data ,get_lexicon
from hmm import get_HMM
from viterbi import decode
from evaluation import eval_model
import random
import csv

train_set = get_data("corpus.xml")[:50]
#test_set = get_data("corpus.xml")[3000:]
lexicon = get_lexicon("lexicon.txt")
model = get_HMM(train_set, lexicon)

results = eval_model(train_set, model)

print("train set: full corpus")
print("sent acc: ",results["sent_accuracy"])
print("     acc: ",results["accuracy"])

with open("confusion.csv","w") as confusion:
    writer = csv.writer(confusion, quoting=csv.QUOTE_ALL)
    writer.writerows(results["confusion"].items())

"""
#print("\nworst_tags\n",results["worst_tags"])
#print("\nworst_words:\n",results["worst_words"])
#print("confusion matrix:")
#print(results["confusion"].tabulate())
"""
