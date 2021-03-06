# Part I - the magic trick
# Gina asks the user to translate a bunch of sentences and goes on to deduce a few syntax
# rules in that language. Very rudimentary but it sure was tough (and fun) to design :D
#
# Written by Deepraj Pandey

import re, string
import numpy as np

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


def print_syntax_rules(LN_Tokens):
    # Print the word order of this language
    SVO = {}
    # [0][0] to flatten the array into an integers
    # Subject changes in sentence 0 and 4
    sub_change = np.where(LN_Tokens[0] != LN_Tokens[4])
    if sub_change[0].size == 0:
        SVO[20] = 'Position of the subject could not be determined from input.'
    else:
        sub_pos = sub_change[0][0]
    
    # Verb in 0 and 7
    v_change = np.where(LN_Tokens[0] != LN_Tokens[7])
    if v_change[0].size == 0:
        SVO[21] = 'Position of the verb could not be determined from input.'
    else:
        verb_pos = v_change[0][0]
    
    # Object in third and fourth
    o_change = np.where(LN_Tokens[0] != LN_Tokens[5])
    if o_change[0].size == 0:
        SVO[22] = 'Position of the object could not be determined from input.'
    else:
        object_pos = o_change[0][0]
        # If the differing string is < 2 in length, it's probably just an article
        if len(LN_Tokens[0][object_pos]) <= 2:
            arr1 = LN_Tokens[0]
            arr2 = LN_Tokens[5]
            # Replace the text with the same text
            np.put(arr1, object_pos, 'sm')
            np.put(arr2, object_pos, 'sm')
            # And look for the next diff
            object_pos = np.where(arr1 != arr2)[0][0]

    # using the position in the sentence as a key (string only) and storing the value
    if sub_change[0].size != 0:
        SVO[sub_pos] = 'Subject'
    if v_change[0].size != 0:
        SVO[verb_pos] = 'Verb'
    if o_change[0].size != 0:
        SVO[object_pos] = 'Object'
    
    print("\nIn your language, the SOV order is", end = ' ')
    for key in sorted(SVO.keys()):
        print('%s' % SVO[key], end = ', ')

    # Print the position of preposition wrt nouns
    
    # Get the noun that is constant in the preposition case
    # from when we parsed object
    if o_change[0].size != 0:
        noun_p = LN_Tokens[0][object_pos]

        largest = -1
        for word in LN_Tokens[1]:
            # Since the JW distance will always be between 0 and 1,
            # this will ensure we are looking at all the distances
            # Note: larger the JW distance, closer are the strings
            dist = jaro_winkler_distance(noun_p, word)
            if dist > largest:
                largest = dist
                # The noun must have changed it's position as preposition might come with morphemes
                new_noun1_index_p = np.where(word == LN_Tokens[1])[0][0]

        largest = -1
        for word in LN_Tokens[3]:
            # Since the JW distance will always be between 0 and 1,
            # this will ensure we are looking at all the distances
            # Note: larger the JW distance, closer are the strings
            dist = jaro_winkler_distance(noun_p, word)
            if dist > largest:
                largest = dist
                # The noun must have changed it's position as preposition might come with morphemes
                new_noun2_index_p = np.where(word == LN_Tokens[3])[0][0]

    # Faulty user input - exact input for 0 and 5
    else:
        # Whatever remains the same is noun - fail safe
        temp_lst = list(set(LN_Tokens[1]).intersection(LN_Tokens[3]))
        temp_lst.sort(key=len, reverse=True)
        # Assuming the longest string will be the noun
        nn = temp_lst[0]
        new_noun1_index_p = np.where(nn == LN_Tokens[1])[0][0]
        new_noun2_index_p = np.where(nn == LN_Tokens[3])[0][0]
        
    
    mid1 = len(LN_Tokens[1])/2
    mid2 = len(LN_Tokens[3])/2
    if (new_noun1_index_p < mid1 and new_noun2_index_p < mid2):
        print("\nyour prepositions usually come after nouns (postpositions),")
    # >= since mid/2 and not mid/2-1
    # Assuming max difference of 1 between num of elements in sen 1 and sen 3
    elif (new_noun1_index_p >= mid1 and new_noun2_index_p >= mid2):
        print("\nyour prepositions usually come before nouns,")
    else:
        print("PN/NP couldn't be determined with the data currently available.")
    
    
    
    # Print the adjective-noun rule
    if sub_change[0].size != 0:
        # Get the unchanging noun
        noun_ad = LN_Tokens[4][sub_pos]
        
        # Adpositions change in seventh and ninth sentence
        largest = -1
        for word in LN_Tokens[6]:
            # Since the JW distance will always be between 0 and 1,
            # this will ensure we are looking at all the distances
            # Note: larger the JW distance, closer are the strings
            dist = jaro_winkler_distance(noun_ad, word)
            if dist > largest:
                largest = dist
                new_noun1_index_a = np.where(word == LN_Tokens[6])[0][0]
        # Noun changes in seventh and ninth
        new_noun2_index_a = np.where(LN_Tokens[6] != LN_Tokens[8])[0][0]
    
    # Faulty user input - subject does not change. Have to resort to basics
    else:
        # Noun changes in seventh and ninth sentence
        new_noun1_index_a = new_noun2_index_a = np.where(LN_Tokens[6] != LN_Tokens[8])[0][0]

    # Whatever remains the same is the adjective
    temp_lst = list(set(LN_Tokens[6]).intersection(LN_Tokens[8]))
    temp_lst.sort(key=len, reverse=True)
    # Assuming the longest string will be the adj
    ad = temp_lst[0]
    adj_pos = np.where(ad == LN_Tokens[6])[0][0]
    if (new_noun1_index_a < adj_pos and new_noun2_index_a < adj_pos):
        print("and adjectives usually come after nouns.")
    elif (new_noun1_index_a > adj_pos and new_noun2_index_a > adj_pos):
        print("and adjectives usually come before nouns.")
    else:
        print("AN/NA couldn't be determined with the data currently available.")

# End of the syntax_rules function


# Subject changes in 0,4 (use noun from 4 for AN)
# Verb changes in 0,7
# Object changes in 0,5 (use noun from 0 for PN)
# Preposition changes in 1,3
# Adjective changes in 6, 8
EN_Sentences = ["The girl eats the banana.", "Near the banana?", "The small fly.", "On top of the banana?", "The fly eats the banana.", "The girl eats the fly.", "The sad fly.", "The girl throws the banana.", "The sad girl."]
LN_Sentences = []
LN_Tokens = []
# Regex to strip input of punctuation
regex = re.compile('[%s]' % re.escape(string.punctuation))

# Get the user translated inputs if the program is run explicitly
if __name__ == '__main__':
    # We have also included the user inputs in different languages from our few rounds of Alpha Testing.
    # Credits: our friends who contributed with these sentences
    # Hindi
    #LN_Sentences = ["Ladki kela khaati hai.", "Kele ke paas?", "Chhoti makhi.", "Kele ke upar.", "Makhi kela khaati hai.", "Ladki makhi khaati hai.", "Dukhi makhi.", "Ladki kela fenkti hai.", "Dukhi ladki."]
    # Odia
    #LN_Sentences = ["Jhia ta kadali khae.", "Kadali pakhare?", "Chhota machhi.", "Kadali upare?", "Machhi ta kadali khae.", "Jhia ta machhi khae.", "Dukhi machhi.", "Jhia ta kadali phopade.", "Dukhi jhia."]
    # Bengali
    #LN_Sentences = ["Meye ta kola khacche.", "Kolar kache?", "Chhoto machhi", "Kolar opor?", "Machhi ta kola khacche", "Meye ta machhi khacche", "Dukhi machhi", "Meye ta kola felche", "Dukhi meye"]
    # French
    #LN_Sentences = ["la fille mange la banane", "pres de la banane", "la petite mouche", "sur la banane", "la mouche mange la banane", "la fille mange la mouche", "la mouche triste", "la fille jet la banane", "la fille triste"]
    # Spanish
    #LN_Sentences = ["La chica come el platano", "Cerca del platano?", "Una pequena mosca", "Encima del platano", "La mosca come el platano", "La chica come la mosca", "La mosca triste", "La chica lanza el platano", "La chica triste"]
    # Marwari
    #LN_Sentences = ["tabari kela khaaye se", "kele ke bagalma", "chhoti makhi", "kele ke upar", "makhi kela khaaye se", "tabari makhi khaaye se", "dukhi makhi", "tabari kela feke hai", "dukhi tabari"]
    # Punjabi
    #LN_Sentences = ["Kudi kela khandi hai.", "kele de kol?", "chhoti makkhi.", "Kele de upar?", "Makkhi kela khandi hai.", "Kudi makkhi khandi hai.", "udas makkhi.", "Kudi kela sutt-di hai.", "Udas Kudi."]
    # Kannada
    #LN_Sentences = ["hudugi balehannannu tintale.", "balehannina hatra?", "chikka nona.", "balehannina mele?", "nona balehannannu tinnatte.", "hudugi nonavannu tintale.", "duhkhi nona.", "hudugi balehannannu esitale.", "duhkhi hudugi."]
    # Kashmiri
    #LN_Sentences = ["koor chhe kel khewan.", "kelas nish.", "laket mechh.", "kelas peyth.", "mechh chhe kel khewan.", "koor chhe mechh khewan.", "udaas mechh.", "koor chhe kel chhakan.", "udaas koor."]
    
    for sentence in EN_Sentences:
       print("Sentence in English: " + sentence)
       h_input = input("Enter translation in your language: ")
       LN_Sentences.append(h_input)

    # Tokenise the inputs. LN_Tokens = [['hello','world']['sentence','two']]
    for h_st in LN_Sentences:
        # Change all the words to lowercase to avoid difference between cases like 'Noun' and 'noun'
        tokenize = np.array(regex.sub('', h_st).lower().split())
        LN_Tokens.append(tokenize)

    # Now, send the tokenised form to
    print_syntax_rules(LN_Tokens)
