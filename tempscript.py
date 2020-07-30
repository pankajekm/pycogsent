import pandas
from nltk.stem import PorterStemmer

positiveTerms = dict()
negativeTerms = dict()
neutralTerms = dict()
f = PorterStemmer()

with open("pycogsent/data/dictionaries/effectwordnet/goldStandard.tff", "r") as fr:
    for i in fr:
        effect = float(i.split('\t')[0]) / 100000000.0
        sentiment = i.split('\t')[1]
        words = i.split('\t')[2].split(',')
        for j in words:
            if (sentiment == '+Effect'):
                positiveTerms[f.stem(j)] = effect
            elif (sentiment == '-Effect'):
                negativeTerms[f.stem(j)] = effect
            else :
                neutralTerms[f.stem(j)] = effect

with open("pycogsent/data/dictionaries/effectwordnet/EWNP.tff", "w") as fr:
    for i in positiveTerms:
        fr.write(i + " " + str(positiveTerms[i]) + "\n")

with open("pycogsent/data/dictionaries/effectwordnet/EWNN.tff", "w") as fr:
    for i in negativeTerms:
        fr.write(i + " " + str(negativeTerms[i]) + "\n")

with open("pycogsent/data/dictionaries/effectwordnet/EWNO.tff", "w") as fr:
    for i in neutralTerms:
        fr.write(i + " " + str(neutralTerms[i]) + "\n")