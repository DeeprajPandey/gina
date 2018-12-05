import os, re, string, json, sys
from collections import OrderedDict

# This statement ensures that any statement in the 'if' block gets executed only if interface.py is executed explicitly on the command line.
# This helps us to use interface as a module to be imported, if need be
if __name__ == "__main__":
    # We don't need to ignore punctuations in the english input here, because when the API is called, the PUNCT tag is specifically skipped
    # in the rest of the python programs
    lex_dict = OrderedDict()
    check = '1'
    orig_words = 0
    word_count = 0
    end_word_count = 0
    word_list = []
    # We ask the user to input till they wish to stop. Also, after every input, we ask them if they wish to see the lexicon that Gina has developed
    while check == '1':
        with open('JSON/lexicon.json', 'r') as f: #calling lexicon.json for read and storing it into a dictionary
            lex_dict = json.loads(f.read())
        for category in lex_dict:
            for key in lex_dict[category]:
                orig_words = orig_words + 1

        enInput = input("Enter your english string.\n")
        regex = re.compile('[%s]' % re.escape(string.punctuation)) # Using regex to ignore punctuation in the text input
        word_list = (regex.sub('', enInput)).split() # Store the non-punctuated english sentence's words in a list
        for elem in word_list:
            for categ in lex_dict:
                for indiv in lex_dict[categ]:
                    if elem == indiv:
                        word_count = word_count + 1
        h_Input = input("\nEnter your hindi string.\n")
        hInput = regex.sub('', h_Input)
        pos_cmd = "python3 pos.py %s" % enInput
        adj_cmd = "python3 Adjectives.py %s" % hInput
        adp_cmd = "python3 Adpositions.py %s" % hInput
        noun_cmd = "python3 Nouns.py %s" % hInput
        verb_cmd = "python3 Verbs.py %s" % hInput
        exam_cmd = "python3 exam.py"
        os.system(pos_cmd)
        os.system(adj_cmd)
        os.system(adp_cmd)
        os.system(noun_cmd)
        os.system(verb_cmd)

        while True: # This loops till the user wants to enter more sentences, on which case it exits the loop and goes back to the start of the outer loop
            os.system("cls||clear") # Clears the screen cls is for windows and clear for Mac and Linux
            print("\n=====================================================================================================")
            print("| Enter the corresponding number to choose an option from below.                                    |")
            print("=====================================================================================================")
            print("| 1. Enter more sentences for Gina to learn from.                                                   |")
            print("| 2. Print all the nouns that Gina knows.                                                           |")
            print("| 3. Print all the verbs that Gina knows.                                                           |")
            print("| 4. Print all the adjectives that Gina knows.                                                      |")
            print("| 5. Print all the prepositions that Gina knows.                                                    |")
            print("| 6. Print all the pronouns that Gina knows.                                                        |")
            print("| 7. Make Gina take an exam based on whatever has been input and her previously acquired knowledge. |")
            print("| 8. Exit the program.                                                                              |")
            print("=====================================================================================================\n")
            print("Your choice:", end = "")
            check = input(" ")
            if check == '1':
                break
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
                    os.system("cls||clear") # Clears the screen cls is for windows and clear for Mac and Linux
            elif check == '3':
                with open('JSON/lexicon.json', 'r') as f: #calling lexicon.json for read and storing it into a dictionary
                    temp_dict = json.loads(f.read())

                print("\n--------------------------------------------------------")
                print("|  {:<12} {:<18} {:<18}  |".format('Noun','Male Inflection','Female Inflection'))
                print("--------------------------------------------------------")
                for verb in temp_dict["verbs"]:
                    print("|  {:<12} {:<18} {:<18}  |".format(verb, temp_dict["verbs"][verb][0], temp_dict["verbs"][verb][1]))
                print("--------------------------------------------------------\n")

                r = input("Press enter to go back to the menu.")
                if r == "":
                    os.system("cls||clear") # Clears the screen cls is for windows and clear for Mac and Linux
            elif check == '6':
                os.system("cls||clear") # Clears the screen cls is for windows and clear for Mac and Linux
                with open('JSON/lexicon.json', 'r') as f: #calling lexicon.json for read and storing it into a dictionary
                    temp_dict = json.loads(f.read())

                print("\n-----------------------------")
                print("|  {:<12} {:<10}  |".format('Pronoun','Hindi Key'))
                print("-----------------------------")
                for pronoun in temp_dict["pronouns"]:
                    if isinstance(temp_dict["pronouns"][pronoun], list):
                        for i in range(len(temp_dict["pronouns"][pronoun])):
                            print("|  {:<12} {:<10}  |".format(pronoun, temp_dict["pronouns"][noun][0]))
                    else:
                        print("|  {:<12} {:<10}  |".format(pronoun, temp_dict["pronouns"][pronoun]))
                print("-----------------------------\n")

                r = input("Press enter to go back to the menu.")
                if r == "":
                    os.system("cls||clear") # Clears the screen cls is for windows and clear for Mac and Linux
            elif check == '7':
                os.system(exam_cmd)
                with open('JSON/lexicon.json', 'r') as f: #calling lexicon.json for read and storing it into a dictionary
                    temp_dict = json.loads(f.read())
                for category in temp_dict:
                    for key in temp_dict[category]:
                        end_word_count = end_word_count + 1
                words_learnt = end_word_count - orig_words

                # Prints the progress bar
                count = (float)(words_learnt/word_count)
                total = 100
                suffix = 'learned.'
                bar_len = 50
                filled_len = int(round(bar_len * count / float(total)))

                percents = round(100.0 * count / float(total), 1)
                bar = '=' * filled_len + '-' * (bar_len - filled_len)

                sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', suffix))
                sys.stdout.flush()

                print("\nPress enter to go back to the menu.")
                r = input("")
                if r == "":
                    os.system("cls||clear") # Clears the screen cls is for windows and clear for Mac and Linux
            elif check == '8':
                os.system("cls||clear") # Clears the screen cls is for windows and clear for Mac and Linux
                sys.exit()
