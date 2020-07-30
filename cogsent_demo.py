import pycogsent as cs
lm=cs.LM()
fn = cs.EWN()
sentence = "The perplexing amount of pollution in the atmosphere is a big wrench in the cogs of life."

print(lm.getScore(sentence))
print(fn.getScore(sentence))