import re, string
import numpy as np

# See how "far" two strings are from each other, character-wise
def hamming_distance(s1, s2):
    # Ensure length of s1 >= s2
    if len(s2) > len(s1):
        s1, s2 = s2, s1
    
    # Distance is difference in length + differing chars
    distance = len(s1) - len(s2)
    for i, c in enumerate(s2):
        if c != s1[i]:
            distance += 1

return distance

# sherlock and watson are the 2 strings we will be dealing with today
def jaro_winkler_distance(sherlock, watson):
    sherlock_len = len(sherlock)
    watson_len = len(watson)
    
    if not sherlock_len or not watson_len:
        return 0.0
    
    # According to Jaro similarity, 2 characters are matching
    # only if they are same and in the range defined below in `search_range`
    min_len = max(sherlock_len, watson_len)
    search_range = (min_len // 2) - 1
    # Negative search_range was a bug for hours. Ugh.
    if search_range < 0:
        search_range = 0

    # Array of flags corresponding to each character, which will toggle to True
    # when they match b/w the strings
    sherlock_flags = [False]*sherlock_len
    watson_flags = [False]*watson_len


# While searching only within the search_range, count & flag matched pairs
common_chars = 0
    for i, sherlock_ch in enumerate(sherlock):
        low = i - search_range if i > search_range else 0
        hi = i + search_range if i + search_range < watson_len else watson_len - 1
        for j in range(low, hi+1):
            # if flag has been toggled to True, we continue
            if not watson_flags[j] and watson[j] == sherlock_ch:
                sherlock_flags[i] = watson_flags[j] = True
                common_chars += 1
                # If a common character is found, again
                # compare the next character in sherlock with the range in watson
                break

# If no characters match, m=0
if not common_chars:
    return 0.0
    
    # Count transpositions
    # Note: only check order of matched characters.
    # For instance, DwAyNE and DuANE have 0 transpositions since the
    # matching letters (range-wise as well) D,A,N,E are in same order.
    k = trans_count = 0
    for i, sherlock_f in enumerate(sherlock_flags):
        if sherlock_f:
            for j in range(k, watson_len):
                if watson_flags[j]:
                    k = j + 1
                    break
            # Means matching but at different positions
            if sherlock[i] != watson[j]:
                trans_count += 1
    # We counted once for each character in sherlock.
    # If transpositions exist, they're counted twice
    trans_count /= 2
    
    # Adjust for similarities in nonmatched characters
    common_chars = float(common_chars)
    # Jaro Distance
    weight = ((common_chars/sherlock_len + common_chars/watson_len +
               (common_chars-trans_count) / common_chars)) / 3
        
               # Winkler modification: continue to boost if strings are similar
               if weight > 0.7 and sherlock_len > 3 and watson_len > 3:
                   # adjust for up to first 4 chars in common
                   j = min(min_len, 4)
                   i = 0
                       while i < j and sherlock[i] == watson[i] and sherlock[i]:
                           i += 1
                               if i:
                                   # The scaling factor, p, is usually 0.1
                                   weight += i * 0.15 * (1.0 - weight)

return weight


def print_syntax_rules(HN_tokens):
    SVO = {}
    # [0][0] to flatten the array into an integers
    # Subject changes in first 2 sentences
    sub_pos = np.where(HN_tokens[0] != HN_tokens[4])[0][0]
    # Verb in second and third
    verb_pos = np.where(HN_tokens[0] != HN_tokens[7])[0][0]
    # Object in third and fourth
    # object_pos = np.where(HN_tokens[0] != HN_tokens[5])[0][0]
    object_pos = np.where(HN_tokens[0] != HN_tokens[5])[0][0]
    arr1 = []
    arr2 = []
    flag = False
    if len(HN_tokens[0][object_pos]) <= 2:
        flag = True
        arr1 = np.delete(HN_tokens[0], object_pos)
        arr2 = np.delete(HN_tokens[5], object_pos)
        object_pos = np.where(arr1 != arr2)[0][0]
    
    # using the position in the sentence as a key (string only) and storing the value
    SVO[sub_pos] = 'Subject'
    SVO[verb_pos] = 'Verb'
    SVO[object_pos] = 'Object'
    
    print("\nIn your language, SVO order is", end = ' ')
    for key in sorted(SVO.keys()):
        print('%s' % SVO[key], end = ', ')
    
    # Get the noun that is constant in the preposition case
    # from when we parsed object
    if flag:
        noun_p = arr1[object_pos].lower()
    else:
        noun_p = HN_tokens[0][object_pos].lower()
    
    for word in HN_tokens[1]:
        if jaro_winkler_distance(noun_p, word.lower()) >= 0.9 and hamming_distance(noun_p, word.lower()) <= 1:
            # The noun must have changed it's position as preposition might come with morphemes
            new_noun_index_p = np.where(word == HN_tokens[1])[0][0]

mid1 = len(HN_tokens[1])/2
mid2 = len(HN_tokens[3])/2
if (new_noun_index_p < mid1 and new_noun_index_p < mid2):
    print("\nprepositions come after Nouns (postpositions),")
    elif (new_noun_index_p >= mid1 and new_noun_index_p >= mid2):
        print("\nprepositions come before Nouns,")
else:
    print("PN/NP couldn't be determined with the data currently available.")
    
    # Adpositions change in third and seventh
    # ad_pos = np.where(HN_tokens[2] != HN_tokens[6])[0][0]
    
    # Get the unchanging noun
    noun_ad = HN_tokens[4][sub_pos].lower()
    
    for word in HN_tokens[2]:
        if jaro_winkler_distance(noun_ad, word.lower()) >= 0.9 and hamming_distance(noun_ad, word.lower()) <= 1:
            # The noun must have changed it's position as preposition might come with morphemes
            new_noun_index_a = np.where(word == HN_tokens[2])[0][0]
    
    mid1 = len(HN_tokens[2])/2
    mid2 = len(HN_tokens[6])/2
    if (new_noun_index_a <= mid1 and new_noun_index_a <= mid2):
        print("and adjectives come before nouns.")
    elif (new_noun_index_a > mid1 and new_noun_index_a > mid2):
        print("and adjectives come after nouns.")
    else:
        print("AN/NA couldn't be determined with the data currently available.")

# Subject changes in 0,4 (use noun from 4 for AN)
# Verb changes in 0,7
# Object changes in 0,5 (use noun from 0 for PN)
# Preposition changes in 1,3
# Adjective changes in 2,6
EN_Sentences = ["The girl eats the banana.", "Near the banana?", "The small fly.", "On top of the banana?", "The fly eats the banana.", "The girl eats the fly.", "The sad fly.", "The girl throws the banana.", "The sad girl."]
HN_Sentences = []
HN_tokens = []
# Regex to strip input of punctuation
regex = re.compile('[%s]' % re.escape(string.punctuation))

# Get the user translated inputs if the program is run explicitly
if __name__ == '__main__':
    # Hindi
    #HN_Sentences = ["Ladki kela khaati hai.", "Kele ke paas?", "Chhoti makhi.", "Kele ke upar.", "Makhi kela khaati hai.", "Ladki makhi khaati hai.", "Dukhi makhi.", "Ladki kela fenkti hai.", "Dukhi ladki."]
    # Odia
    #HN_Sentences = ["Jhia ta kadali khae.", "Kadali pakhare?", "Chhota machhi.", "Kadali upare?", "Machhi ta kadali khae.", "Jhia ta machhi khae.", "Dukhi machhi.", "Jhia ta kadali phopade.", "Dukhi jhia."]
    # Bengali
    #HN_Sentences = ["Meye ta kola khacche.", "Kolar kache?", "Chhoto machhi", "Kolar opor?", "Machhi ta kola khacche", "Meye ta machhi khacche", "Dukhi machhi", "Meye ta kola felche", "Dukhi meye"]
    # French
    #HN_Sentences = ["la fille mange la banane", "pres de la banane", "la petite mouche", "sur la banane", "la mouche mange la banane", "la fille mange la mouche", "la mouche triste", "la fille jet la banane", "la fille triste"]
    # Spanish
    #HN_Sentences = ["La chica come el platano", "Cerca del platano?", "Una pequena mosca", "Encima del platano", "La mosca come el platano", "La chica come la mosca", "La mosca triste", "La chica lanza el platano", "La chica triste"]
    # Marwari
    #HN_Sentences = ["tabari kela khaaye se", "kele ke bagalma", "chhoti makhi", "kele ke upar", "makhi kela khaaye se", "tabari makhi khaaye se", "tabari kela feke hai", "tabari kela feke hai", "dukhi tabari"]
    # Punjabi
    #HN_Sentences = ["Kudi kela khandi hai.", "kele de kol?", "chhoti makkhi.", "Kele de upar?", "Makkhi kela khandi hai.", "Kudi makkhi khandi hai.", "udas makkhi.", "Kudi kela sutt-di hai.", "Udas Kudi."]
    
    for sentence in EN_Sentences:
        print("Sentence in English: " + sentence)
        h_input = input("Enter translation in your language: ")
        HN_Sentences.append(h_input)
    # Tokenise the inputs. HN_tokens = [['hello','world']['sentence','two']]
    for h_st in HN_Sentences: 
        tokenize = np.array(regex.sub('', h_st).split())
        HN_tokens.append(tokenize)

    # Now, send the tokenised form to 
    print_syntax_rules(HN_tokens)
