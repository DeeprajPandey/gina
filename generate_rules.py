import re, string
import numpy as np
EN_Sentences = ["The girl eats the banana.", "The fly eats the banana."]
HN_Sentences = ["Ladki ne kela khaya.", "Ladke ne kela khaya."]
HN_tokens = []
regex = re.compile('[%s]' % re.escape(string.punctuation))
# We know that the subject changes in the first two sentences.
# Let's find the changing word in the hindi sentences and store their position.
for h_st in HN_Sentences:
	tokenize = np.array(regex.sub('', h_st).split())
	HN_tokens.append(tokenize)
print(np.where(HN_tokens[0] != HN_tokens[1]))