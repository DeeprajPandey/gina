import re, string
import numpy as np

def print_SVO_rules(HN_tokens):
    SVO = {}
    PN = {}
    # [0][0] to flatten the arrays into an integers
    # Subject changes in first 2 sentences
    sub_pos = np.where(HN_tokens[0] != HN_tokens[1])[0][0]
    # Verb in second and third
    verb_pos = np.where(HN_tokens[1] != HN_tokens[2])[0][0]
    # Object in third and fourth
    object_pos = np.where(HN_tokens[2] != HN_tokens[3])[0][0]

    # using the position in the sentence as a key (string only) and storing the value
    SVO[sub_pos] = 'Subject'
    SVO[verb_pos] = 'Verb'
    SVO[object_pos] = 'Object'
    
    # Get the noun we are using in the next two sentences
    noun = HN_tokens[3][object_pos]
    # The noun must have changed it's position as preposition might come with morphemes
    new_noun_index = np.where(noun == HN_tokens[4])[0][0]
    
    # Preposition changes in fifth and sixth
    # Store the index of the pre/post-position
    prep_pos = np.where(HN_tokens[4] != HN_tokens[5])[0][0]
    
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
EN_Sentences = ["The girl eats the banana.", "The fly eats the banana.", "The fly throws the banana", "The fly throws the fruit.", "The fly is near the fruit.", "The fly is on top of the fruit."]
HN_Sentences = ["Ladki ne kela khaya.", "Makhi ne kela khaya.", "Makhi ne kela feka.", "Makhi ne fal feka.", "Makhi fal ke paas hai", "Makhi fal ke upar hai."]
HN_tokens = []
# Regex to strip input of punctuation
regex = re.compile('[%s]' % re.escape(string.punctuation))
# Tokenise the inputs. HN_tokens = [['hello','world']['sentence','two']]
for h_st in HN_Sentences:
    tokenize = np.array(regex.sub('', h_st).split())
    HN_tokens.append(tokenize)

# Now, send the tokenised form to 
print_SVO_rules(HN_tokens)