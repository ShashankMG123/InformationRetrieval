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
    esKeys = [int(i) for i in id]
    # print(finalRes)
    resKeys = list([i in esKeys for i in finalRes.keys()])

    esKeys = [True] * len(esKeys)

    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for i in range(len(resKeys)):
        if(resKeys[i] == esKeys[i]):
            if(resKeys[i]):
                TP += 1
            else:
                TN += 1
        else:
            if(resKeys[i]):
                FP += 1
            else:
                FN += 1


    print("----------CONFUSION MATRIX------------")
    print([TP,FP])
    print([FN,TN])
    print("-----------------METRICS-----------------")
    acc = (TP+TN)/(TP+TN+FP+FN)
    prec = (TP)/(TP+FP)
    recall = (TP)/(TP+FN)
    f1score = (2*prec*recall) / (prec+recall)

    print("Accuracy :", acc)
    print("Precision :", prec)
    print("Recall :", recall)
    print("FScore :", f1score)

    