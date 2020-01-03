from corpus import get_data ,get_lexicon
from hmm import get_HMM
from viterbi import decode
from evaluation import eval_model
import random
import pandas as pd

print("EVALUATION FOR HALF OF CORPUS WORDS APPEARING ONLY ONCE TURNED INTO UNK TOKEN\n")

# setting up data
data = random.shuffle(get_data("corpus.xml"))
train_set = get_data("corpus.xml")[:3300]
test_set = get_data("corpus.xml")[3300:]
lexicon = get_lexicon("lexicon.txt")

# training the model
model = get_HMM(train_set, lexicon)

# evaluation on train data
results = eval_model(train_set, model)

df = pd.DataFrame(results["confusion"]).fillna(0)
df.to_csv('train_confusion.csv')
c = [ item[0] for item in results["worst_tags"][:10] ]
s = [ item[0] for item in results["worst_codes"][:10] ]
print("################# TRAININ EVALUATION ################")
print("\n")
print("sent acc: ",results["sent_accuracy"])
print("     acc: ",results["accuracy"])
print("\nCommon confusions:\n")
print(results["confusion"].tabulate( conditions = c, samples = s ) )


# evaluation on test data
results = eval_model(test_set, model)

df = pd.DataFrame(results["confusion"]).fillna(0)
df.to_csv('test_confusion.csv')
c = [ item[0] for item in results["worst_tags"][:10] ]
s = [ item[0] for item in results["worst_codes"][:10] ]
print("\n\n\n################# TEST EVALUATION ################")
print("\n")
print("sent acc: ",results["sent_accuracy"])
print("     acc: ",results["accuracy"])
print("\nCommon confusions:\n")
print(results["confusion"].tabulate( conditions = c, samples = s ) )

