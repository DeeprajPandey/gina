import json, sys
from collections import OrderedDict

lex_dict = OrderedDict()
exam_question = input("\nEnter a word to check if Gina knows about it.\n")
with open('JSON/lexicon.json', 'r') as f: #calling lexicon.json for read and storing it into a dictionary
    lex_dict = json.loads(f.read())

for noun, noun_info in lex_dict["nouns"].items():
    if exam_question == noun:
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
        sys.exit()



for verb, verb_info in lex_dict["verbs"].items():
    if exam_question == verb:
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
        sys.exit()


for adj, adj_info in lex_dict["adjectives"].items():
    if exam_question == adj:
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
        sys.exit()


for adp, adp_info in lex_dict["adpositions"].items():
    if exam_question == adp:
        print("Preposition: " + adp)
        print("Postposition:", end = " ")
        if adp_info == "":
            print("Unknown")
        else:
            print(adp_info)
        sys.exit()

    if pronoun == list(lex_dict["pronouns"].keys())[-1]:
        print("Word: Unknown")
    else
        check = input("Is this correct? (y) - yes or (n) or no")
        if check == 'n'
            
