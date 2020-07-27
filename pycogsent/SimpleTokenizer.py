import re
class SimpleTokenizer():
    def tokenize(self,text):
        pattern=r"[\w']+"
        return re.findall(pattern, text.lower())

if __name__ == "__main__":
    ss=SimpleTokenizer()
    print(ss.tokenize("This is bad because of  misplaced and damage beyond"))