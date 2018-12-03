import re, string
import numpy as np
# Subject changes in 0,1
# Verb changes in 1,2
# Object changes in 2,3
EN_Sentences = ["The girl eats the banana.", "The fly eats the banana.", "The fly throws the banana", "The fly throws the fruit."]
HN_Sentences = ["Ladki ne kela khaya.", "Makhi ne kela khaya.", "Makhi ne kela feka.", "Makhi ne fal feka."]
HN_tokens = []
# Regex to strip input of punctuation
regex = re.compile('[%s]' % re.escape(string.punctuation))
# Tokenize the inputs. HN_tokens = [['hello','world']['sentence','two']]
for h_st in HN_Sentences:
    tokenize = np.array(regex.sub('', h_st).split())
    HN_tokens.append(tokenize)
#print(np.sum(HN_tokens[0] == HN_tokens[1]))
# Subject changes in the first two sentences.
# Find the changing word in the hindi sentences and store their position.
SVO = {}
# [0][0] to flatten the arrays into an integers
sub_pos = np.where(HN_tokens[0] != HN_tokens[1])[0][0]
verb_pos = np.where(HN_tokens[1] != HN_tokens[2])[0][0]
object_pos = np.where(HN_tokens[2] != HN_tokens[3])[0][0]

# using the position in the sentence as a key (string only) and storing the value
SVO[np.array_str(sub_pos)] = 'Subject'
SVO[np.array_str(verb_pos)] = 'Verb'
SVO[np.array_str(object_pos)] = 'Object'