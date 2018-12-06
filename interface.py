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
    while True: # This loops till the user wants to exit the program
        os.system("clear") # Clears the screen
        print("\n=====================================================================================================")
        print("| Enter the corresponding number to choose an option from below.                                    |")
        print("=====================================================================================================")
        print("| 1. Teach Gina!                                                                                    |")
        print("| 2. View the nouns that Gina knows.                                                                |")
        print("| 3. View the verbs that Gina knows.                                                                |")
        print("| 4. View the adjectives that Gina knows.                                                           |")
        print("| 5. View the prepositions that Gina knows.                                                         |")
        print("| 6. View the the pronouns that Gina knows.                                                         |")
        print("| 7. Test Gina!                                                                                     |")
        print("| 8. Exit the program.                                                                              |")
        print("=====================================================================================================\n")
        print("Your choice:", end = "")
        check = input(" ")
        os.system("clear") # Clears the screen
        if check == '1':
            # We don't need to ignore punctuations in the english input here, because when the API is called, the PUNCT tag is specifically skipped
            # in the rest of the python programs
            # We ask the user to input till they wish to stop. Also, after every input, we ask them if they wish to see the lexicon that Gina has developed
            with open('JSON/lexicon.json', 'r') as f: #calling lexicon.json for read and storing it into a dictionary
                lex_dict = json.loads(f.read())
            for category in lex_dict:
                for key in lex_dict[category]:
                    orig_words = orig_words + 1

            print("Give Gina an English sentence:\n")
            enInput = input("")
            regex = re.compile('[%s]' % re.escape(string.punctuation)) # Using regex to ignore punctuation in the text input
            word_list = (regex.sub('', enInput)).split() # Store the non-punctuated english sentence's words in a list
            for elem in word_list:
                for categ in lex_dict:
                    for indiv in lex_dict[categ]:
                        if elem == indiv:
                            word_count = word_count + 1
            print("\nGive Gina its Hindi translation:\n")
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
            os.system(exam_cmd)

            with open('JSON/lexicon.json', 'r') as f: #calling lexicon.json for read and storing it into a dictionary
                temp_dict = json.loads(f.read())
            for category in temp_dict:
                for key in temp_dict[category]:
                    end_word_count = end_word_count + 1
            words_learnt = end_word_count - orig_words

            print("\n")
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
        elif check == '2':
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
        elif check == '3':
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
        elif check == '4':
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
        elif check == '5':
            with open('JSON/lexicon.json', 'r') as f: #calling lexicon.json for read and storing it into a dictionary
                temp_dict = json.loads(f.read())

            print("\n-----------------------------")
            print("|  {:<12} {:<10}  |".format('Preposition','Postposition'))
            print("-----------------------------")
            for prep in temp_dict["adpositions"]:
                print("|  {:<12} {:<10}  |".format(prep, temp_dict["adpositions"][prep]))
            print("-----------------------------\n")

            r = input("Press enter to go back to the menu.")
            if r == "":
                os.system("clear") # Clears the screen
        elif check == '6':
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
        elif check == '7':
            os.system(exam_cmd)
            print("\nPress enter to go back to the menu.")
            r = input("")
            if r == "":
                os.system("clear") # Clears the screen
        elif check == '8':
            sys.exit()
