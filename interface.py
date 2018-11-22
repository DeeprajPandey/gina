import os

if __name__ == "__main__":
    usrInput = input("Enter your english string.\n")
    h_accept = input("\nEnter your hindi string.\n")
    hTrans = h_accept.split()
'''
    with open(“temp.txt”, w) as f:
        f.write(e_accept)
        f.write(h_accept)

with open(“temp.txt”, r) as f:
    str = f.readline()
    h_output = f.readline(2)
text = h_output.split()
'''
os.system("python pos.py")
os.system("python Adjectives.py")
os.system("python Adpositions.py")
os.system("python Nouns.py")
os.system("python Verbs.py")
