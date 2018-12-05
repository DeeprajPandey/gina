import os, re, string, json, sys
from collections import OrderedDict

# This statement ensures that any statement in the 'if' block gets executed only if interface.py is executed explicitly on the command line.
# This helps us to use interface as a module to be imported, if need be
if __name__ == "__main__":
    # We don't need to ignore punctuations in the english input here, because when the API is called, the PUNCT tag is specifically skipped
    # in the rest of the python programs
    lex_dict = OrderedDict()
    check = '1'
    # We ask the user to input till they wish to stop. Also, after every input, we ask them if they wish to see the lexicon that Gina has developed
    while check == '1':
        enInput = input("Enter your english string.\n")
        h_Input = input("\nEnter your hindi string.\n")
        regex = re.compile('[%s]' % re.escape(string.punctuation)) # Using regex to ignore punctuation in the hindi text input
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
            print("\n=====================================================================================================")
            print("| Enter the corresponding number to choose an option from below.                                    |")
            print("=====================================================================================================")
            print("| 1. Enter more sentences for Gina to learn from.                                                   |")
            print("| 2. Print all the pronouns that Gina knows.                                                        |")
            print("| 3. Make Gina take an exam based on whatever has been input and her previously acquired knowledge. |")
            print("| 4. Exit the program.                                                                              |")
            print("=====================================================================================================\n")
            print("Your choice:", end = "")
            check = input(" ")
            if check == '1':
                break
            elif check == '2':
                print("\n---------------------------------")
                print("|  Pronoun\tHindi Key\t|")
                print("---------------------------------")
                with open('JSON/lexicon.json', 'r') as f: #calling lexicon.json for read and storing it into a dictionary
                    lex_dict = json.loads(f.read())
                    for pronoun in lex_dict["pronouns"]:
                        if isinstance(lex_dict["pronouns"][pronoun], list):
                            for i in range(len(lex_dict["pronouns"][pronoun])):
                                print("|  " + pronoun + "\t\t" + lex_dict["pronouns"][pronoun][i] + "\t\t|")
                        else:
                            print("|  " + pronoun + "\t\t" + lex_dict["pronouns"][pronoun] + "\t\t|")
                print("---------------------------------\n")
                r = input("Press enter to go back to the menu.")
                if r == "":
                    os.system("cls") # Clears the screen
            elif check == '3':
                os.system(exam_cmd)
                r = input("Press enter to go back to the menu.")
                if r == "":
                    os.system("cls") # Clears the screen
            elif check == '4':
                os.system("cls") # Clears the screen
                sys.exit()
