import pandas
from pycogsent.basepredictor import BasePredictor
from pycogsent.config import DATA_PATH
from pycogsent.SimpleStemmer import SimpleStemmer

class EFN(BasePredictor):

    DICT_PATH = "%s/dictionaries/effectwordnet/goldStandard.tff"%DATA_PATH
    _stemmer = SimpleStemmer()

    def init_dictionary(self):
        positiveTerms = dict()
        negativeTerms = dict()
        neutralTerms = dict()
        with open(self.DICT_PATH, "r") as flstream:
            for i in flstream:
                effect = float(i.split('\t')[0]) / 100000000.0
                sentiment = i.split('\t')[1]
                words = i.split('\t')[2].split(',')
                for j in words:
                    if (sentiment == '+Effect'):
                        positiveTerms[self._stemmer.stemWord(j)] = effect
                    elif (sentiment == '-Effect'):
                        negativeTerms[self._stemmer.stemWord(j)] = effect
                    else :
                        neutralTerms[self._stemmer.stemWord(j)] = effect
        self._positiveTerms = positiveTerms
        self._negativeTerms = negativeTerms
        self._neutralTerms = neutralTerms

    def _getScore(self, token):
        if(token in self._positiveTerms.keys()):
            return 1
        if(token in self._negativeTerms.keys()):
            return -1
        return 0