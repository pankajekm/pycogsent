import pycogsent as cs
lm=cs.LM()
sentence = "He is the perpetrator."

print(lm.getScore(sentence))