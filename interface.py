import os

if __name__ == "__main__":
    enInput = input("Enter your english string.\n")
    hInput = input("\nEnter your hindi string.\n")
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
