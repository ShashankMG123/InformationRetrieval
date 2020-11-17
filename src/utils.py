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

def compareOutputs(finalRes, id):
    esKeys = set([int(i) for i in id])
    resKeys = set(finalRes.keys())
    # print(esKeys)
    # print(resKeys)

    TP = len(esKeys.intersection(resKeys))
    FP = len(resKeys.difference(esKeys))
    TN = 0
    FN = len(esKeys.difference(resKeys))

    print("\n----------CONFUSION MATRIX------------")
    print([TP,FP])
    print(f"[{FN}, X]")
    print("\n-----------------METRICS-----------------")
    acc = (TP+TN)/(TP+TN+FP+FN)

    # handling a border case which has zero TP and FP
    # which if not handled gives a zero division error. 
    if not TP and not FP:
        prec = 0
    else:
        prec = (TP)/(TP+FP)
    
    # similar to precision, recall division error is handled below.
    if not TP and not FN:
        recall = 0
    else:
        recall = (TP)/(TP+FN)

    # if both precision and recall is zero, f1-score is set to zero.
    if not prec and not recall:
        f1score = 0
    else:
        f1score = (2*prec*recall) / (prec+recall)

    print("Accuracy :", acc)
    print("Precision :", prec)
    print("Recall :", recall)
    print("FScore :", f1score)

    