from corpus import get_data ,get_lexicon
from hmm import get_HMM
from viterbi import decode
from evaluation import eval_model
import random

train_set = get_data("corpus.xml")[:3000]
test_set = get_data("corpus.xml")[3000:]
lexicon = get_lexicon("lexicon.txt")
model = get_HMM(train_set, lexicon)

results = eval_model(train_set, model)

print("train set: corpus[:3000]")
print("\nworst_tags\n",results["worst_tags"])
print("\nworst_words:\n",results["worst_words"])
print("\nacc: ",results["accuracy"])
#print("confusion matrix:")
#print(results["confusion"].tabulate())


results = eval_model(test_set, model)
print("test set: corpus[3000:] ")
print("\nworst_tags\n",results["worst_tags"])
print("\nworst_words:\n",results["worst_words"])
print("\nacc: ",results["accuracy"])
#print("confusion matrix:")
#print(results["confusion"].tabulate())
