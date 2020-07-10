import nltk
class SimpleTokenizer():
    def tokenize(self,text):
        pattern="[\w']+"

        return nltk.regexp_tokenize(text.lower(), pattern)
if __name__ == "__main__":
    ss=SimpleTokenizer()
    print(ss.tokenize("This is bad because of  misplaced and damage beyond"))