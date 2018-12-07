#Part II: Niyati
# json for Google Language API and lexicon
# sys for accepting the string as command line argument when the file is called
import json, sys
#PREPOSITIONS
#MAJOR ASSUMPTION: USER WILL ENTER THE ENTIRE PREPOSITION JAMMED INTO ONE WORD
#Function has: EST, HST. Access to all lexicons.
#EST = [[token, tag]]
#HST = [token]
# Get the part of speech specific lexicon from the main JSON
with open('JSON/lexicon.json', 'r') as fp:
    lexicon_dict = json.loads(fp.read())
#NOUNLEXICON: Englishkey : [nominative_inflection, grammatical_gender, accusative_inflection]
Noun_Lexicon = lexicon_dict['nouns'] #G: M, F, U.
#VERBLEXICON: Englishkey : [male_inflection, female_inflection, person] Person: if the English is in 'First Person' or 'Third Person'
Verb_Lexicon = lexicon_dict['verbs']
#ADJECTIVELEXICON: Englishkey :  [male_inflection, female_inflection, accusative_inflection]
ADJ_Lexicon = lexicon_dict['adjectives']
#ADPOSITIONLEXICON: Englishkey : postposition
ADP_Lexicon = lexicon_dict['adpositions']
#PRONOUNLEXICON: Englishkey: Hindikey
Pronoun_Lexicon = lexicon_dict['pronouns'] #Print this and provide spelling to user, ask user to separate mujh ko.
#EST = [['The', 'DET'], ['you', 'PRON'],['write', 'VERB'], ['on', 'ADP'], ['big', 'ADJ'], ['and', 'CONJ'],['fat', 'ADJ'], ['cat', 'NOUN']]
# Part III - code for reading from partsOfSpeech.json and creating the nested list, EST and taking command line args for HST, done by Abhinav Masalia
EST = []
with open('JSON/partsOfSpeech.json', 'r') as f: #calling partsOfSpeech.json for read and storing it into a dictionary
    pos_dict = json.loads(f.read())

for x in pos_dict["tokens"]:
    row = []
    if x["partOfSpeech"]["tag"] == "PUNCT":#not storing punctuation marks in EST
        continue #if a "PUNCT" is encountered, then the nothing is appended and
    row.append(x["text"]["content"])
    row.append(x["partOfSpeech"]["tag"])
    EST.append(row)

h_arg = ''
h_index=0 #to keep track of the index of the program name so that it isn't taken into account as a string
for x in sys.argv: #taking the hindi text from the command line and storing into a variable
    if(h_index != 0): #this is required to skip the name of the program from the command line
        h_arg = h_arg + x + ' '
    h_index=1
HST = h_arg.split() #splits individual words into a list which is stored in HST
# Part III ends

HST_size = len(HST)
EST_size = len(EST)
index=-1;
for word in EST:
	index=index+1
	search_index= index+1 #start searching for the noun from the next position
	updated = False #whether the postposition has been learnt
	if(word[1]=='ADP' and word[0] not in ADP_Lexicon):
		while(search_index < EST_size and updated==False):
			Current_word=EST[search_index][0]
			Current_word_tag = EST[search_index][1]
			if(Current_word_tag=='NOUN' and Current_word in Noun_Lexicon and Noun_Lexicon[Current_word][2] != ''): #if we know the accusative inflection of the noun
				Hindi_Acc = Noun_Lexicon[Current_word][2] # noun with postposition appears in the accusative_inflection in Hindi: kutte par, ladki kebaadmein
				HST_index = 0
				found =False
				Current_word_h = ''
				for Hindi_word in HST:
					if(Hindi_word == Hindi_Acc):
						Current_word_h = Hindi_word
						found = True
				if(found):
					HST_index = HST.index(Current_word_h) #found the noun
					HST_index = HST_index +1 #the postposition will always be EXACTLY after the noun in Hindi, because all the adjectives will come before; verbs etc come after the Adpositional Phrase
					if(HST[HST_index]=='ke'): #many postpositions will do this: table ke upar, neeche, etc.
						HST_index = HST_index +1
					Hindi_ADP = HST[HST_index]
					ADP_Lexicon.update({word[0]: Hindi_ADP})
					updated = True
			search_index = search_index+1
# Load the updated lexicon to the file
updated_lex = {
    "nouns": Noun_Lexicon,
    "verbs": Verb_Lexicon,
    "adjectives": ADJ_Lexicon,
    "adpositions": ADP_Lexicon,
    "pronouns": Pronoun_Lexicon
}
with open('JSON/lexicon.json', 'w') as fp:
    json.dump(updated_lex, fp, indent = 2)
