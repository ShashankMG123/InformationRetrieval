from nltk import bigrams, pad_sequence
import pickle
import os
from BTrees.OOBTree import OOBTree


# Takes input as a pickle path generated pickle file with corresponding bigrams.
# pad left with $
# pad right with $

# ($,'a'): ["abcd"]
# ('a','b'): ["abcd"]

"""
Function that builds the bigram index similar to the above example
takes in a single pickle file of inverted index
build a biGram dictionary as a BTree
"""
def createBiGramPickle(pickleFile):
    with open(f'../indexes/{pickleFile}', 'rb') as file:
        invertedIndex = pickle.load(file)

    biGramDict = OOBTree()
    # taking the key of the inverted index (vocab words)
    # using inbuilt library bigrams to generate bigrams
    # and also pad them with $ in the start and end of the word
    for key in invertedIndex.keys():
        bigramKey = list(bigrams(list(pad_sequence(key,
                                        pad_left=True, left_pad_symbol="$",
                                        pad_right=True, right_pad_symbol="$", 
                                        n=2))))
        # this part is basically to write the bigrams
        # into the BTree based on the key
        for i in bigramKey:
            if(not biGramDict.has_key(i)):
                biGramDict.insert(i, [key])
            else:
                biGramDict[i].append(key)
    # generating a pickle file for the bigram generated
    with open(f'../bigramIndex/{pickleFile[:-7]}.pickle', 'wb') as handle:
        pickle.dump(biGramDict, handle, protocol=pickle.HIGHEST_PROTOCOL)

all_filenames = os.listdir("../indexes/")
# reading all the pickle files one byb one and 
# calling the generate bigram function
for i in range(len(all_filenames)):
    createBiGramPickle(all_filenames[i])
