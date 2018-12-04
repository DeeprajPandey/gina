# json for Google Language API and lexicon
# sys for accepting the string as command line argument when the file is called
import json, sys
#ADJECTIVES
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

HST_size = len(HST)
EST_size = len(EST)
index=-1;
for word in EST:
	index=index+1
	if((word[1]=='ADJ' and word[0] not in ADJ_Lexicon) or (word[1]=='ADJ' and word[0] in ADJ_Lexicon and (ADJ_Lexicon[word[0]][0]=='' or ADJ_Lexicon[word[0]][1]=='' or ADJ_Lexicon[word[0]][2]==''))): #UNKNOWN Adjective or known adjective with unknown parameters
		search_index = index +1
		updated = False
		Cannot_be_learned=True
		if(word[0] in ADJ_Lexicon):
			Saved_Male_Inflection = ADJ_Lexicon[word[0]][0]
			Saved_Female_Inflection = ADJ_Lexicon[word[0]][1]
			Saved_Accusative_Inflection = ADJ_Lexicon[word[0]][2]
		else:
			Saved_Male_Inflection=''
			Saved_Female_Inflection=''
			Saved_Accusative_Inflection=''
		while(search_index < EST_size and updated==False):
			#print(word[0])
			
			Current_word=EST[search_index][0]
			#print(Current_word)
			Current_word_tag = EST[search_index][1]
			if(Current_word_tag=='NOUN' and Current_word in Noun_Lexicon and Cannot_be_learned==True):
				Hindi_Nom = Noun_Lexicon[Current_word][0] #nominative_inflection: bada kutta
				Hindi_Acc = Noun_Lexicon[Current_word][2] #accusative_inflection: bade kutte ko
				Hindi_G = Noun_Lexicon[Current_word][1] #accusative_inflection
				HST_index = 0
				found =False
				Current_word_h = ''
				for Hindi_word in HST:
					if(Hindi_word == Hindi_Nom or Hindi_word == Hindi_Acc):
						Current_word_h = Hindi_word
						found = True
				#To count the distance between the adjective and the noun: the only thing that can come in the middle is more adjectives, and maybe 'and' or 'but'
				ADJ_count=0
				ADJ_index = index
				#print(index)
				#print(EST[ADJ_index][1])
				Only_ADJ=True #only adjectives may be present
				while(EST[ADJ_index][1] != 'NOUN'):
					if(EST[ADJ_index][1]=='ADJ'):
						ADJ_count = ADJ_count +1
					elif(EST[ADJ_index][1]!='CONJ'): #'and' can be between adjectives
						Only_ADJ = False
					ADJ_index = ADJ_index+1
				#print(ADJ_count)
				if(found and Only_ADJ):
					HST_index = HST.index(Current_word_h)
					#to skip interceding adjectives
					skipper = 0
					while(skipper<ADJ_count):
						HST_index= HST_index-1
						skipper = skipper+1
						if(HST[HST_index] == 'aur' or HST[HST_index] == 'or' or HST[HST_index] == 'aar' or HST[HST_index] == 'lekin' or HST[HST_index] == 'par'): #consecutive adjectives in Hindi may be interlocuted by 'and' and 'but'
							HST_index= HST_index-1
					H_ADJ = HST[HST_index]

					if(Current_word_h == Hindi_Nom):
						CASE = 'NOM'
					elif(Current_word_h == Hindi_Acc):
						CASE= 'ACC'
					if(Hindi_G=='F'):
						if(not H_ADJ.endswith('ee') and not H_ADJ.endswith('i')):
							ADJ_Lexicon.update({word[0]: [H_ADJ, H_ADJ, H_ADJ]}) #all inflections same for adjectives like 'drudh' or 'sundar'
						else:
							ADJ_Lexicon.update({word[0]: [Saved_Male_Inflection, H_ADJ, Saved_Accusative_Inflection]}) #nominative, accusative same for female
						updated = True
					elif(Hindi_G=='M'):
						if(not H_ADJ.endswith('e') and not H_ADJ.endswith('a')):
							ADJ_Lexicon.update({word[0]: [H_ADJ, H_ADJ, H_ADJ]}) #nominative, accusative same for male nouns not ending in 'a', same as female!
							updated = True
						else:
							if(CASE=='NOM'):
								ADJ_Lexicon.update({word[0]: [H_ADJ, Saved_Female_Inflection, Saved_Accusative_Inflection]})
								updated=True
							if(CASE=='ACC'):
								ADJ_Lexicon.update({word[0]: [Saved_Male_Inflection, Saved_Female_Inflection, H_ADJ]})
								updated=True
			if(Current_word_tag=='NOUN' and Current_word not in Noun_Lexicon):
				Cannot_be_learned=True #if we do not know the noun right after adjective, we cannot learn this adjective from other nouns! Must abort
			search_index = search_index +1
		if(updated == False):
			if(EST[index-1][0]=='is' or EST[index-1][0]=='turns' or EST[index-1][0]=='becomes' or EST[index-1][0]=='am' ):
				E_noun = EST[index-2][0]; #e.g. in 'the sky is blue'
				if(E_noun in Noun_Lexicon and Noun_Lexicon[E_noun][0] != ''):
					H_noun = Noun_Lexicon[E_noun][0]
					#print(H_noun)
					#print(HST)
					if(H_noun not in HST):
						break
					HN_index = HST.index(H_noun)
					G=Noun_Lexicon[E_noun][1]
					HA_index=HN_index+1;
					H_ADJ=HST[HA_index];
					if(G=='F'):
						if(not H_ADJ.endswith('ee') and not H_ADJ.endswith('i')):
							ADJ_Lexicon.update({word[0]: [H_ADJ, H_ADJ, H_ADJ]}) #all inflections same for adjectives like 'drudh' or 'sundar'
						else:
							ADJ_Lexicon.update({word[0]: [Saved_Male_Inflection, H_ADJ, Saved_Accusative_Inflection]}) #nominative, accusative same for female
						updated = True
					if(G=='M'):
						if(not H_ADJ.endswith('e') and not H_ADJ.endswith('a')):
							ADJ_Lexicon.update({word[0]: [H_ADJ, H_ADJ, H_ADJ]}) #nominative, accusative same for male nouns not ending in 'a', same as female!
							updated = True
						else:
							ADJ_Lexicon.update({word[0]: [H_ADJ, Saved_Female_Inflection, Saved_Accusative_Inflection]}) #nominative, accusative same for female
							updated=True
					if(G=='U'):
						if(H_ADJ.endswith('a')):
							ADJ_Lexicon.update({word[0]: [H_ADJ, Saved_Female_Inflection, Saved_Accusative_Inflection]}) #nominative, accusative same for female
							updated=True
						if(H_ADJ.endswith('i') or H_ADJ.endswith('ee')):
							ADJ_Lexicon.update({word[0]: [Saved_Male_Inflection, H_ADJ, Saved_Accusative_Inflection]}) #nominative, accusative same for female
							updated=True
				if(E_noun in Pronoun_Lexicon):
					if(E_noun!='you'):
						H_noun = Pronoun_Lexicon[E_noun]
					else:
						H_noun = Pronoun_Lexicon[E_noun][0]
					if(H_noun not in HST):
						break
					HN_index = HST.index(H_noun)
					HA_index=HN_index+1;
					H_ADJ=HST[HA_index];
					if(H_ADJ.endswith('a')):
						ADJ_Lexicon.update({word[0]: [H_ADJ, Saved_Female_Inflection, Saved_Accusative_Inflection]}) #nominative, accusative same for female
						updated=True
					if(H_ADJ.endswith('i') or H_ADJ.endswith('ee')):
						ADJ_Lexicon.update({word[0]: [Saved_Male_Inflection, H_ADJ, Saved_Accusative_Inflection]}) #nominative, accusative same for female
						updated=True
					if(updated==False)
						ADJ_Lexicon.update({word[0]: [H_ADJ, H_ADJ, H_ADJ]}) #nominative, accusative same for female
						updated=True
					
		

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
