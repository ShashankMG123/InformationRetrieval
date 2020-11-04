import json
import pickle
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

def nltk_tag_to_wordnet_tag(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:          
        return None

def lemmatize_sentence(sentence):
    #tokenize the sentence and find the POS tag for each token
    lemmatizer = WordNetLemmatizer()
    nltk_tagged = pos_tag(sentence)  
    #tuple of (token, wordnet_tag)
    wordnet_tagged = map(lambda x: (x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            #if there is no available tag, append the token as is
            lemmatized_sentence.append(word)
        else:        
            #else use the tag to lemmatize the token
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    return lemmatized_sentence

def openOnePair(fileName):
    with open(f'../documentInfo/{fileName}.json', 'r') as f:
            docInfo = json.load(f)

    with open(f"../indexes/{fileName}.pickle", 'rb') as file:
        invertedIndex = pickle.load(file)
    
    return [docInfo , invertedIndex]


def openBigram(fileName):
    with open(f"../bigramIndex/{fileName}.pickle", 'rb') as file:
        bigramIndex = pickle.load(file)
    return bigramIndex