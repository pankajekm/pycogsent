from config import DATA_PATH
from SimpleStemmer import SimpleStemmer
import pandas as pd
def getFirstToken(text):
    ss=SimpleStemmer()
    return ss.stem(text.lower())
def convertLM():
    PATH = '%s/dictionaries/LM.csv' % DATA_PATH
    POS_PATH = '%s/dictionaries/LMP.csv' % DATA_PATH
    NEG_PATH = '%s/dictionaries/LMN.csv' % DATA_PATH
    data = pd.read_csv(PATH)
    _positiveTerms = set(data.query('Positive > 0')['Word'].apply(getFirstToken).dropna())
    _negativeTerms = set(data.query('Negative > 0')['Word'].apply(getFirstToken).dropna())
    negativeTerms=",".join(_negativeTerms)
    positiveTerms=",".join(_positiveTerms)
    POS_FILE = open(POS_PATH,"w")
    NEG_FILE = open(NEG_PATH,"w")
    POS_FILE.write(positiveTerms)
    NEG_FILE.write(negativeTerms)
    POS_FILE.close()
    NEG_FILE.close()

if __name__ == "__main__":
    convertLM()