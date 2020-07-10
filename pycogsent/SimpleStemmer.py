
from nltk.stem import PorterStemmer
class SimpleStemmer():
    ps=PorterStemmer()
    def stem(self,text):
        return self.stemWord(text)
    def stemWord(self,text):
        return self.ps.stem(text)
    def stemWords(self,tokens):
        
        return list(map(self.stemWord,tokens))
if  __name__ == "__main__":
    "testing"
    ss=SimpleStemmer()
    print(ss.stemWord("going"))
    print(ss.stemWords("We are going there".split()))