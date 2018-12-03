import re, string
import numpy as np

# See how "far" two strings are from each other, character-wise
def hamming_distance(str1, str2):
    # Ensure length of s1 >= s2
    if len(str2) > len(str1):
        str1, str2 = str2, str1

    # Distance is difference in length + differing chars
    distance = len(str1) - len(str2)
    for i, c in enumerate(str2):
        if c != str1[i]:
            distance += 1

    return distance


def print_SVO_rules(HN_tokens):
    SVO = {}
    PN = {}
    # [0][0] to flatten the arrays into an integers
    # Subject changes in first 2 sentences
    sub_pos = np.where(HN_tokens[0] != HN_tokens[4])[0][0]
    # Verb in second and third
    verb_pos = np.where(HN_tokens[0] != HN_tokens[7])[0][0]
    # Object in third and fourth
    object_pos = np.where(HN_tokens[0] != HN_tokens[5])[0][0]

    # using the position in the sentence as a key (string only) and storing the value
    SVO[sub_pos] = 'Subject'
    SVO[verb_pos] = 'Verb'
    SVO[object_pos] = 'Object'
    
    # Get the noun we are using in the next two sentences
    noun = HN_tokens[0][object_pos]
    
    for word in HN_tokens[1]:
        if hamming_distance(noun, word) <= 1:
            # The noun must have changed it's position as preposition might come with morphemes
            new_noun_index = np.where(word == HN_tokens[1])[0][0]
    
    # Preposition changes in fifth and sixth
    # Store the index of the pre/post-position
    prep_pos = np.where(HN_tokens[1] != HN_tokens[3])[0][0]
    
    if prep_pos < new_noun_index:
        print("Prepositions come before Nouns in your language.")
    elif prep_pos > new_noun_index:
        print("Prepositions come after Nouns in your language (postpositions).")
    else:
        print("PN/NP couldn't be determined with the data currently available.")

    for key in sorted(SVO.keys()):
        print('%s' % SVO[key], end = ' ')

# Subject changes in 0,1
# Verb changes in 1,2
# Object changes in 2,3
EN_Sentences = ["The girl eats the banana.", "The fly is near the banana.", "The small fly.", "The fly is on top of the banana.", "The fly eats the banana.", "The girl eats the fly.", "The sad fly.", "The girl throws the banana.", "The sad girl."]
HN_Sentences = ["Ladki ne kela khaya.", "Makhi kele ke paas hai", "Chhoti makhi.", "Makhi kele ke upar hai.", "Makhi ne kela khaya.", "Ladki ne makhi khaya.", "Dukhi makhi.", "Ladki ne kela feka.", "Dukhi ladki."]
HN_tokens = []
# Regex to strip input of punctuation
regex = re.compile('[%s]' % re.escape(string.punctuation))
# Tokenise the inputs. HN_tokens = [['hello','world']['sentence','two']]
for h_st in HN_Sentences:
    tokenize = np.array(regex.sub('', h_st).split())
    HN_tokens.append(tokenize)

# Now, send the tokenised form to 
print_SVO_rules(HN_tokens)
