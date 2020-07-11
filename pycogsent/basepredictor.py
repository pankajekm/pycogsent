import os
import re
import numpy as np
import abc
import nltk
from pycogsent.SimpleTokenizer import SimpleTokenizer
from pycogsent.SimpleStemmer import SimpleStemmer
from pycogsent.config import DATA_PATH
# DATA_PATH = "/home/pankaj/Documents/Python Projects/pycogsent/data"

class BasePredictor(object):
    __metaclass__ = abc.ABCMeta
    EPSILON = 1e-6

    def __init__(self,tokenizer=None):
        self._positiveTerms = set()
        self._negtiveTerms = set()
        if tokenizer is not None:
            self._tokenizer = tokenizer
        else:
            self._tokenizer=SimpleTokenizer()
        self.init_dictionary()
        self._stemmer=SimpleStemmer()


        
        assert len(self._positiveTerms) > 0 and len(self._negativeTerms) > 0

    def tokenize(self,text):
        return self._tokenizer.tokenize(text)
        
    "Remove if not needed"     
    def tokenizer(self,text):
        return re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', text) 

    def getFirstToken(self, tokens):
        return tokens.split(",")[0]

    @abc.abstractmethod
    def init_dictionary(self):
        pass

    def _getScore(self,token):
        print(token)
        if token in self._positiveTerms:
            print("pos")
            return 1
        print(self._negativeTerms)
        if token in self._negativeTerms:
            print("neg")
            return -1
        print("neutral")
        return 0

    def stemWords(self,tokens):
        return self._stemmer.stemWords(tokens)

    def getScore(self,text):
        tokens=self.tokenize(text.lower())
        for token in tokens:
            print(token)
        stemmedTokens= self.stemWords(tokens)
        print(stemmedTokens)
        #print(self._positiveTerms)
        print( "unpaid" in self._negativeTerms)
        scores=np.array(list(map(self._getScore,stemmedTokens)))
        positiveScore= np.sum(scores[scores > 0])
        negativeScore = -np.sum(scores[scores < 0])
        polarity = (positiveScore-negativeScore) * 1.0 / ((positiveScore+negativeScore)+self.EPSILON)
        subjectivity = (positiveScore+negativeScore) * 1.0 / (len(scores)+self.EPSILON)
        
        return {"Positive Score": positiveScore,
                "Negative Score": negativeScore,
                "Polarity": polarity,
                "Subjectivity": subjectivity}
    
    
        