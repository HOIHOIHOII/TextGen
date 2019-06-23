# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 09:38:07 2019

@author: AI
"""

#A very naive idea of what predicting the next word in a sentence might look like

#idea 1 (and maybe the only idea) 
#Bayesian analysis

#write a word parsing function

#get a text, get couplet frequencies

#for the purposes of answering the question "What word is next?", assign priors
#based on what word/s have come before

import re
import numpy as np
from collections import Counter

def read_book(file, start, end):
    """read digital book and return contents """
    with open(file,"r", encoding = "utf8") as f:
        book = ""
        first_content_line = start
        last_content_line = end
        i = 1
        for line in f: 
            if i >= last_content_line:
                break
            elif i >= first_content_line:
                book = book + line
                i = i+1
            else:
                i = i+1
        print("{} is {} lines long, including {} non-content lines at the start".format(file, i, first_content_line))
    return book


def very_basic_parse(text):
    """very simple text parsing. This makes something worse than single character parse."""
    text = text.replace("\n"," ")
    text = text.replace("“"," ")
    text = text.replace("”"," ")
    text = text.replace("."," ")
    text = text.replace("\""," ")
    text = text.replace(",","")
    text = text.replace(";"," ")
    text = text.replace("?"," ")
    text = text.replace("!"," ")
    text = text.replace("_"," ")
    text = text.replace("--"," ")
    text = text.replace("'"," ")
    text = text.replace("  "," ")
    text = text.lower()
    tokens = text.split(" ")
    tokens = [word for word in tokens if word not in ['','s']]
    return tokens

def simple_parse(text):
    """even simpler, just look at individual characters"""
    return text.split()

def create_word_pairs(parsed_text):
    """create a list of every pair of words that occur beside each other, ignoring punctuation"""
    pairs = []
    previous_word = None
    for i, word in enumerate(parsed_text):
        if previous_word is None:
            pass
        else:
            pair = "{0} {1}".format(previous_word, word)
            pairs.append(pair)
        previous_word = word
    return pairs


#process books
PandP_JA = read_book("PandP_JA.txt", 38, 13062)
MansfieldPlace_JA = read_book("MansfieldPlace_JA.txt",42, 15378)
Emma_JA = read_book("Emma_JA.txt",43, 16263)
NorthangerAbbey_JA = read_book("NorthangerAbbey_JA.txt",58, 7871)
Persuasion_JA = read_book("Persuasion_JA.txt",48, 8360)
SenseAndSensibility_JA = read_book("SenseAndSensibility_JA.txt",465, 13283)

#create data structures
all_books = PandP_JA+MansfieldPlace_JA+Emma_JA+NorthangerAbbey_JA+Persuasion_JA+SenseAndSensibility_JA
full_text_parsed = simple_parse(all_books)
print("Here's a sample of the text parse:", full_text_parsed[0:50])

pairs = create_word_pairs(full_text_parsed)
pair_count = Counter(pairs)
couplet_frequency_dict = {key:{} for key, val in Counter(full_text_parsed).items()}

for pair, count in pair_count.items():
    word1, word2 = pair.split(" ")
    couplet_frequency_dict[word1][word2] = count

#print(couplet_frequency_dict["from"])

def predict(word, pair_frequency_dict):
    """uses pair frequency counts to make a weighted random choice of the next word"""
    words, counts = list(zip(*(pair_frequency_dict[word].items())))
    total = sum(counts)
    freqs= [count/total for count in counts]
    next_word = np.random.choice(words, p=freqs)
    return next_word

print({key:val for key, val in Counter(pairs).items() if val > 100})
    
print(predict("how", couplet_frequency_dict))

def talk_to_me(seed_word,pair_frequency_dict, sentence_length):
    """creates a sentence by predicting one word after the next"""
    sentence = [seed_word]
    for _ in range(sentence_length):
        next_word = predict(sentence[-1], pair_frequency_dict)
        sentence.append(next_word)
    sentence_str = " ".join(sentence)
    return sentence_str

print(talk_to_me("Miss", couplet_frequency_dict, 200 ))

