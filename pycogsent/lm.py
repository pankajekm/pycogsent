import pandas as pd
from pycogsent.basepredictor import DATA_PATH, BasePredictor



class LM(BasePredictor):

    
    POS_PATH = '%s/dictionaries/LMP.csv' % DATA_PATH
    NEG_PATH = '%s/dictionaries/LMN.csv' % DATA_PATH
    
    def init_dictionary(self):
        POS_FILE=open(self.POS_PATH,"r")
        positiveTerms=POS_FILE.read().split(",")
        POS_FILE.close()
        NEG_FILE=open(self.NEG_PATH,"r")
        negativeTerms=NEG_FILE.read().split(",")
        NEG_FILE.close()

        self._positiveTerms = positiveTerms
        self._negativeTerms = negativeTerms
        