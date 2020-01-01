from corpus import get_data #,get_lexicon
from hmm import get_HMM
from viterbi import decode
import random
import nltk


# decode an input
def decode_sentence(s, model):
    return decode(s, model)

# find all errors in a batch
def diagnose_batch(batch, model):
    
    wrong_answers = [ ]
    wrong_tags = [ ]
    wrong_words = [ ]
    #returned_tags = [ ]
    answer_count = 0
    correct_count = 0
    error_count = 0
    #keys_count = 0
    
    for s in batch:
        s["decoded"] = decode_sentence(s, model)
        for i in range(0, s["len"])
            answer_count += 1
            if s["tags"][i] != s["decoded"][i]:
                error_count += 1
                wrong_answers.append( (s["tags"][i],s["decoded"]) )
                wrong_tags.append( s["tags"][i] )
                wrong_words.append( s["tokens"][i] )
            else:
                correct_count += 1
                
    return {
            "wrong_answers": wrong_answers,
            "wrong_tags": wrong_tags,
            "wrong_words": wrong_words,
            "answer_count": answer_count,
            "correct_count": correct_count,
        }

# evaluate a model on a set
def eval_model(batch, model):
    
    diag = diagnose_batch(batch,model)
    
    return {
            "accuracy": diag["correct_count"]/diag["answer_count"] * 100,
            "confusion" : nltk.ConditionalFreqDist(diag["wrong_answers"]),
            "worst_tags": sorted([item[0] for item in nltk.FreqDist(wrong_tags).items()], lambda=item:item[1], reverse=True)[:10],
            "worst_words": sorted([item[0] for item in nltk.FreqDist(wrong_tokens).items()], lambda=item:item[1], reverse=True)[:10],
        }
    
    
