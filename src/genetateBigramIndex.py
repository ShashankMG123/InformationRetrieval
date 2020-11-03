from nltk import bigrams, pad_sequence
import pickle
import os
from BTrees.OOBTree import OOBTree

"""
Takes input as a pickle path generated pickle file with corresponding bigrams.
pad left with <s>
pad right with </s>

(<>,'a'): ["abcd"]
('a','b'): ["abcd"]
.
.
.

"""

def createBiGramPickle(pickleFile):
    with open(f'../indexes/{pickleFile}', 'rb') as file:
        invertedIndex = pickle.load(file)

    biGramDict = OOBTree()

    for key in invertedIndex.keys():
        bigramKey = list(bigrams(list(pad_sequence(key,
                                        pad_left=True, left_pad_symbol="$",
                                        pad_right=True, right_pad_symbol="$", 
                                        n=2))))
        for i in bigramKey:
            if(not biGramDict.has_key(i)):
                biGramDict.insert(i, [key])
            else:
                biGramDict[i].append(key)
    with open(f'../bigramIndex/{pickleFile[:-7]}.pickle', 'wb') as handle:
        pickle.dump(biGramDict, handle, protocol=pickle.HIGHEST_PROTOCOL)

all_filenames = os.listdir("../indexes/")
for i in range(len(all_filenames)):
    createBiGramPickle(all_filenames[i])
