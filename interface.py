import os, re, string

# This statement ensures that any statement in the 'if' block gets executed only if interface.py is executed explicitly on the command line.
# This helps us to use interface as a module to be imported, if need be
if __name__ == "__main__":
    # We don't need to ignore punctuations in the english input here, because when the API is called, the PUNCT tag is specifically skipped
    # in the rest of the python programs
    enInput = input("Enter your english string.\n")
    h_Input = input("\nEnter your hindi string.\n")
    regex = re.compile('[%s]' % re.escape(string.punctuation)) # Using regex to ignore punctuation in the hindi text input
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
