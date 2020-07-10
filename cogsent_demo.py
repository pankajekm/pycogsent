import pycogsent as cs
lm=cs.LM()
sentence="This is bad and good because of  misplaced and damage beyond unpaid"

print(lm.getScore(sentence))