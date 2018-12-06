import json
from collections import OrderedDict

lex_dict = OrderedDict()
exam_question = input("\nEnter a word to check if Gina knows it.\n")
with open('JSON/lexicon.json', 'r') as f: #calling lexicon.json for read and storing it into a dictionary
    lex_dict = json.loads(f.read())

# store where the word is found
category = ""

# Introducing found to see if the word was found and also to have a better way to ask the user in the end if the word asked in the exam is correct
found = True
while True:
    # Iterates through the noun dictionary of lexicon.json to print the information if the input word is found
    for noun, noun_info in lex_dict["nouns"].items():
        if exam_question == noun:
            category = "nouns"
            print("Noun: " + noun)
            print("Gender:", end = " ")
            if noun_info[1] == "F":
                print("Female")
            if noun_info[1] == "M":
                print("Male")
            if noun_info[1] == "U":
                print("Unknown")

            print("Nominative Inflection:", end = " ")
            if noun_info[0] == "":
                print("Unknown")
            else:
                print(noun_info[0])

            print("Accusative Inflection:", end = " ")
            if noun_info[2] == "":
                print("Unknown")
            else:
                print(noun_info[2])
            found = False # This helps check in the end if the word was found or not
            break


    # Iterates through the verb dictionary of lexicon.json to print the information if the input word is found
    for verb, verb_info in lex_dict["verbs"].items():
        if exam_question == verb:
            category = "verbs"
            print("Verb: " + verb)
            print("Person:", end = " ")
            if verb_info[2] == "":
                print("Unknown")
            else:
                print(verb_info[2])

            print("Male Inflection:", end = " ")
            if verb_info[0] == "":
                print("Unknown")
            else:
                print(verb_info[0])

            print("Female Inflection:", end = " ")
            if verb_info[1] == "":
                print("Unknown")
            else:
                print(verb_info[1])
            found = False
            break


    # Iterates through the adjectives dictionary of lexicon.json to print the information if the input word is found
    for adj, adj_info in lex_dict["adjectives"].items():
        if exam_question == adj:
            category = "adjectives"
            print("Adjective: " + adj)
            print("Male Inflection:", end = " ")
            if adj_info[0] == "":
                print("Unknown")
            else:
                print(adj_info[0])

            print("Female Inflection:", end = " ")
            if adj_info[1] == "":
                print("Unknown")
            else:
                print(adj_info[1])

            print("Accusative Inflection:", end = " ")
            if adj_info[2] == "":
                print("Unknown")
            else:
                print(adj_info[2])
            found = False
            break


    # Iterates through the adpositions dictionary of lexicon.json to print the information if the input word is found
    for adp, adp_info in lex_dict["adpositions"].items():
        if exam_question == adp:
            category = "adpositions"
            print("Preposition: " + adp)
            print("Postposition:", end = " ")
            if adp_info == "":
                print("Unknown")
            else:
                print(adp_info)
            found = False
            break

    # We want the while loop only to run once and break out of it on finding a word or if the entire dictionary is traversed, so this break statement serves the purpose
    break

# This means that found = False wasn't encountered i.e. the word wasn't found in Gina's lexicon
if found:
    print("Word: Unknown")
else:
    check = input("\nIs the information learned about the word correct?\n(y) - yes or (n) or no\n")
    if check == 'n' or check == 'no':
        # Deleting the word from Gina's lexicon if the user feels the information learnt by Gina is wrong
        del lex_dict[category][exam_question]
        # Writing back the updated lexicon to lexicon.json
        with open('JSON/lexicon.json', 'w') as f:
            json.dump(lex_dict, f, indent = 2)
        print("Gina removed the word, \"" + exam_question + "\" from her lexicon!")
