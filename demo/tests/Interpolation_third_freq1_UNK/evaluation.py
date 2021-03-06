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
    wrong_codes = [ ]
    wrong_words = [ ]

    answer_count = 0
    error_count = 0
    correct_count = 0
    sent_correct_count = 0
    
    for s in batch:
        sent_correct = True
        s["decoded"] = decode_sentence(s, model)
        for i in range(0, s["len"]):
            answer_count += 1
            if s["tags"][i] != s["decoded"][i]:
                sent_correct = False
                error_count += 1
                wrong_answers.append( (s["tags"][i],s["decoded"][i]) )
                wrong_tags.append( s["tags"][i] )
                wrong_codes.append( s["decoded"][i] )
                wrong_words.append( s["tokens"][i] )
            else:
                correct_count += 1
        if sent_correct:
            sent_correct_count += 1
        
    return wrong_answers, wrong_tags, wrong_codes, wrong_words, answer_count, correct_count, sent_correct_count


# evaluate a model on a set
def eval_model(batch, model):
    
    #diag = diagnose_batch(batch,model)
    wrong_answers, wrong_tags, wrong_codes, wrong_words, answer_count, correct_count, sent_correct_count = diagnose_batch(batch, model)
    
    return {
            "accuracy": correct_count/ answer_count * 100,
            "sent_accuracy": sent_correct_count / len(batch) * 100 ,
            "confusion" : nltk.ConditionalFreqDist( (correct,wrong) for (correct,wrong) in wrong_answers ),
            "worst_tags": sorted([item for item in nltk.FreqDist(wrong_tags).items()], key = lambda item:item[1], reverse=True)[:10],
            "worst_codes": sorted([item for item in nltk.FreqDist(wrong_codes).items()], key = lambda item:item[1], reverse=True)[:10],
            "worst_words": sorted([item for item in nltk.FreqDist(wrong_words).items()], key = lambda item:item[1], reverse=True)[:10],
        }
    
    
