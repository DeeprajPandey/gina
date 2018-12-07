# Code written by Abhinav Masalia
import os, re, string, json, sys
from collections import OrderedDict

# This statement ensures that any statement in the 'if' block gets executed only if interface.py is executed explicitly on the command line.
# This helps us to use interface as a module to be imported, if need be
if __name__ == "__main__":
    lex_dict = OrderedDict()
    orig_words = 0
    word_count = 0
    end_word_count = 0
    word_list = []
    exam_cmd = "python3 exam.py" # Moving it outside the loop, so that the user can directly access the exam without input
    gen_rules = "python3 generate_rules.py"
    while True: # This loops till the user wants to exit the program
        os.system("clear") # Clears the screen
        print("\n======================================================================================================")
        print("| Enter the corresponding number to choose an option from below.                                     |")
        print("======================================================================================================")
        print("|  1. Generate syntax rules for your language.                                                       |")
        print("|  2. Teach Gina!                                                                                    |")
        print("|  3. View the nouns that Gina knows.                                                                |")
        print("|  4. View the verbs that Gina knows.                                                                |")
        print("|  5. View the adjectives that Gina knows.                                                           |")
        print("|  6. View the prepositions that Gina knows.                                                         |")
        print("|  7. View the pronouns that Gina knows.                                                             |")
        print("|  8. Test Gina!                                                                                     |")
        print("|  9. View instructions for teaching Gina.                                                           |")
        print("| 10. Exit the program.                                                                              |")
        print("======================================================================================================\n")
        print("Your choice:", end = "")
        option = input(" ")
        os.system("clear") # Clears the screen
        if option == '1':
            os.system(gen_rules)
            r = input("Press enter to go back to the menu.")
            if r == "":
                os.system("clear") # Clears the screen
        elif option == '2':
            # We don't need to ignore punctuations in the english input here, because when the API is called, the PUNCT tag is specifically skipped
            # in the rest of the python programs
            # We ask the user to input till they wish to stop. Also, after every input, we ask them if they wish to see the lexicon that Gina has developed
            with open('JSON/lexicon.json', 'r') as f: #calling lexicon.json for read and storing it into a dictionary
                lex_dict = json.loads(f.read())
            for category in lex_dict:
                for key in lex_dict[category]:
                    orig_words = orig_words + 1

            print("\nGive Gina an English sentence:", end = " ")
            enInput = input("")
            regex = re.compile('[%s]' % re.escape(string.punctuation)) # Using regex to ignore punctuation in the text input
            word_list = (regex.sub('', enInput)).split() # Store the non-punctuated english sentence's words in a list
            for elem in word_list:
                for categ in lex_dict:
                    for indiv in lex_dict[categ]:
                        if elem == indiv:
                            word_count = word_count + 1
            print("Give Gina its Hindi translation:", end = " ")
            h_Input = input("")
            hInput = regex.sub('', h_Input)
            pos_cmd = "python3 pos.py %s" % enInput
            adj_cmd = "python3 Adjectives.py %s" % hInput
            adp_cmd = "python3 Adpositions.py %s" % hInput
            noun_cmd = "python3 Nouns.py %s" % hInput
            verb_cmd = "python3 Verbs.py %s" % hInput
            os.system(pos_cmd)
            os.system(adj_cmd)
            os.system(adp_cmd)
            os.system(noun_cmd)
            os.system(verb_cmd)

            with open('JSON/lexicon.json', 'r') as f: #calling lexicon.json for read and storing it into a dictionary
                temp_dict = json.loads(f.read())
            for category in temp_dict:
                for key in temp_dict[category]:
                    end_word_count = end_word_count + 1
            words_learnt = end_word_count - orig_words

            # Prints the progress bar
            count = float(words_learnt/word_count)*100
            total = 100
            suffix = 'learned.'
            bar_len = 50
            filled_len = int(round(bar_len * count / float(total)))

            percents = round(100.0 * count / float(total), 1)
            bar = '=' * filled_len + '-' * (bar_len - filled_len)

            sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', suffix))
            sys.stdout.flush()

            print("\n")
            print("Press enter to go back to the menu.", end = "")
            r = input("\n")
            if r == "":
                os.system("clear") # Clears the screen
        elif option == '3':
            with open('JSON/lexicon.json', 'r') as f: #calling lexicon.json for read and storing it into a dictionary
                temp_dict = json.loads(f.read())

            print("\n-----------------------------")
            print("|  {:<12} {:<10}  |".format('Noun','Hindi Key'))
            print("-----------------------------")
            for noun in temp_dict["nouns"]:
                print("|  {:<12} {:<10}  |".format(noun, temp_dict["nouns"][noun][0]))
            print("-----------------------------\n")

            r = input("Press enter to go back to the menu.")
            if r == "":
                os.system("clear") # Clears the screen
        elif option == '4':
            with open('JSON/lexicon.json', 'r') as f: #calling lexicon.json for read and storing it into a dictionary
                temp_dict = json.loads(f.read())

            print("\n--------------------------------------------------------")
            print("|  {:<12} {:<18} {:<18}  |".format('Verb','Male Inflection','Female Inflection'))
            print("--------------------------------------------------------")
            for verb in temp_dict["verbs"]:
                print("|  {:<12} {:<18} {:<18}  |".format(verb, temp_dict["verbs"][verb][0], temp_dict["verbs"][verb][1]))
            print("--------------------------------------------------------\n")

            r = input("Press enter to go back to the menu.")
            if r == "":
                os.system("clear") # Clears the screen
        elif option == '5':
            with open('JSON/lexicon.json', 'r') as f: #calling lexicon.json for read and storing it into a dictionary
                temp_dict = json.loads(f.read())

            print("\n--------------------------------------------------------")
            print("|  {:<12} {:<18} {:<18}  |".format('Adjective','Male Inflection','Female Inflection'))
            print("--------------------------------------------------------")
            for adj in temp_dict["adjectives"]:
                print("|  {:<12} {:<18} {:<18}  |".format(adj, temp_dict["adjectives"][adj][0], temp_dict["adjectives"][adj][1]))
            print("--------------------------------------------------------\n")

            r = input("Press enter to go back to the menu.")
            if r == "":
                os.system("clear") # Clears the screen
        elif option == '6':
            with open('JSON/lexicon.json', 'r') as f: #calling lexicon.json for read and storing it into a dictionary
                temp_dict = json.loads(f.read())

            print("\n----------------------------------")
            print("|  {:<12} {:<15}  |".format('Preposition','Postposition'))
            print("----------------------------------")
            for prep in temp_dict["adpositions"]:
                print("|  {:<12} {:<15}  |".format(prep, temp_dict["adpositions"][prep]))
            print("----------------------------------\n")

            r = input("Press enter to go back to the menu.")
            if r == "":
                os.system("clear") # Clears the screen
        elif option == '7':
            with open('JSON/lexicon.json', 'r') as f: #calling lexicon.json for read and storing it into a dictionary
                temp_dict = json.loads(f.read())

            print("\n-----------------------------")
            print("|  {:<12} {:<10}  |".format('Pronoun','Hindi Key'))
            print("-----------------------------")
            for pronoun in temp_dict["pronouns"]:
                if isinstance(temp_dict["pronouns"][pronoun], list):
                    for i in range(len(temp_dict["pronouns"][pronoun])):
                        print("|  {:<12} {:<10}  |".format(pronoun, temp_dict["pronouns"][pronoun][0]))
                else:
                    print("|  {:<12} {:<10}  |".format(pronoun, temp_dict["pronouns"][pronoun]))
            print("-----------------------------\n")

            r = input("Press enter to go back to the menu.")
            if r == "":
                os.system("clear") # Clears the screen
        elif option == '8':
            os.system(exam_cmd)
            print("\nPress enter to go back to the menu.")
            r = input("")
            if r == "":
                os.system("clear") # Clears the screen
        elif option == '9':
            print("--------------------------------------------------------------------------------------------------------------------------------------------")
            print("| Instructions for teaching Gina                                                                                                           |")
            print("--------------------------------------------------------------------------------------------------------------------------------------------")
            print("|  1. (!)Conjunctions:                                                                                                                     |")
            print("|        i. May be used as connectors of two or more complete sentences,                                                                   |")
            print("|        ii. May be used between adjectives.                                                                                               |")
            print("|        iii. May not be used assuming a trace/parallelism;                                                                                |")
            print("|             e.g. I like the sea and the sun; say rather: I like the sea and I like the sun.                                              |")
            print("|  2. No plural nouns. The sentence, therefore, cannot be ‘The sky and the ocean are blue’.                                                |")
            print("|     This is in essence a plural noun! Simple test: check the verb of the sentence                                                        |")
            print("|  3. (!)No compound/non-singleton noun phrases: these include nouns like the cat’s mother, and also my book.                              |")
            print("|  4. Only simple presenttense usage: e.g. I eat àmain khaati hoon, but not I am eating -> main kha rahi hoon.                             |")
            print("|     For example:                                                                                                                         |")
            print("|     I play -> main khelta hoon                                                                                                           |")
            print("|     She runs -> vah daudti hai                                                                                                           |")
            print("|  5. (!)No English phrasal verbs.                                                                                                         |")
            print("|     A phrasal verb is any verb with another element, typically a preposition: ‘see to’ or an adverb ‘break down’ or both ‘look down on’. |")
            print("|     This also excludes negations of verbs: I do not like you; The sky is not blue, etc. are no tallowed.                                 |")
            print("|  6. English verbs with more than two arguments. For example, Iexplained the problem to you.                                              |")
            print("|  7. (!)Enter jammed Hindi phrasal verbs (in case of an English singleton verb that translates into a phrasal verb in Hindi).             |")
            print("|     I love the tree -> main ped ko pyaar_karti hoon.                                                                                     |")
            print("|  8. (!)No English compound adpositions: these are rare in any case, but do exist: This is over and above what Gina can deal with.        |")
            print("|  9. (!)Enter jammed Hindi compound adpositions, if any.                                                                                  |")
            print("| 10. Consistent spelling in Hindi and English                                                                                             |")
            print("| 11. Adherence to the hardcoded spellings of pronouns; hardcoded verbs is -> hai, am ->hoon                                               |")
            print("| 12. (!)No usage of honorific forms in Hindi: i.e. all sentences must be in the register of the least ‘respectful’ – tu, vah, usko, hai   |")
            print("| 13. No imperatives, questions or fragmented sentences.                                                                                   |")
            print("| 14. In general, simple sentences involving simple units of either language!                                                              |")
            print("--------------------------------------------------------------------------------------------------------------------------------------------")
            r = input("Press enter to go back to the menu.")
            if r == "":
                os.system("clear") # Clears the screen

        elif option == '10':
            os.system("clear") # Clears the screen
            sys.exit()
