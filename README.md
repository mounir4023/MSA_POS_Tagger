# MSA_POS_Tagger
HMM and Transfer learning implementations for modern arabic part of speech tagger using python

# HMM Model
In this first implementation we tried to reproduce the HMM model from "A Hidden Markov Model Based POS Tagger for Arabic, Al Shamsi - Guessoum 2006" using their improved tagset and minimal version of their corpus which they provided us with for studying purposes at University Of Science and Technology Houari Boumediene, Algiers.

project structure:
- corpus.py: code to transform corpus and lexicon text to python dict to use later.
- hmm.py: contains code to parse the corpus and calculate unigram/bigram/trigram counts of tags and emission (tag,word) pairs.
- viterbi.py: second ordrer viterbi decoding algorithm implementation from "Course notes for NLP by Michael Collins, Columbia University"
- evaluation.py: functions to calculate per word and per sentence accuracies.
- accuracy.py: script to calculate the train and test accuracies and confusion matrix of tags.
- test.py: playground file to test new implemented features.
- API/: python-system called perl code provided by the teacher from "Al Shamsi - Guessoum 2006" to tokenize arabic text and split affixes from tokens.
- UTILITY/: preprocessing playgroud code.
- TESTS/: code state and test result from different configurations.
- DEMO/: run python app.py after installing eel package and other dependencies to test the arabic tagger.
- SCREENSHOTS/: some console & app screenshots.

# Transfer Learning Model
Still looking for a pretrained universal language model in arabic to fine tune on POSTagging.
