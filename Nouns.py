# json for Google Language API and lexicon
# sys for accepting the string as command line argument when the file is called
import json, sys
#Still to be addded: Possessors
#NOUNS
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

#EST = [['I', 'PRON'], ['eat', 'VERB'], ['a', 'DET'], ['tree', 'NOUN']]
EST=[]
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
	#print(word[1])
	if((word[1]=='NOUN' and word[0] not in Noun_Lexicon) or (word[1]=='NOUN' and word[0] in Noun_Lexicon and (Noun_Lexicon[word[0]][0]=='' or Noun_Lexicon[word[0]][1]=='U' or Noun_Lexicon[word[0]][2]==''))): #UNKNOWN NOUN or known noun with unknown gender
	#What if the noun is there, but incomplete?
		G='' #grammatical gender
		search_index = index -1
		updated = False
		
		while(search_index > -1 and (updated==False or (Noun_Lexicon[word[0]][0]=='' or Noun_Lexicon[word[0]][1]=='U' or Noun_Lexicon[word[0]][2]==''))): #Going leftwards:
			if(word[0] in Noun_Lexicon):
				Saved_Nominative_Inflection = Noun_Lexicon[word[0]][0]
				Saved_Gender = Noun_Lexicon[word[0]][1]
				Saved_Accusative_Inflection = Noun_Lexicon[word[0]][2]
			else:
				Saved_Nominative_Inflection=''
				Saved_Gender='U'
				Saved_Accusative_Inflection=''
				Current_word = EST[search_index][0]
			Current_word=EST[search_index][0]
			#print(Current_word)
			Current_word_tag = EST[search_index][1]
			#print(Current_word_tag)
			noun_phrase_present=False
			if(Current_word_tag=='ADJ' and Current_word in ADJ_Lexicon):
				Hindi_M = ADJ_Lexicon[Current_word][0] #male_inflection
			#	print(Hindi_M)
				Hindi_F = ADJ_Lexicon[Current_word][1] #female_inflection
			#	print(Hindi_F)
				Hindi_A = ADJ_Lexicon[Current_word][2] #accusative_inflection
			#	print(Hindi_A)
				HST_index = 0
				found =False
				Current_word_h = ''
				for Hindi_word in HST:
					if(Hindi_word == Hindi_F or Hindi_word == Hindi_M or Hindi_word == Hindi_A):
						Current_word_h = Hindi_word
						found = True
				if(found):
					HST_index = HST.index(Current_word_h)
					if(Current_word_h == Hindi_F):
						G = 'F'
					elif(Current_word_h == Hindi_M):
						G = 'M'
					elif(Current_word_h == Hindi_A):
						G = 'M' #ONLY MALE ADJECTIVES INFLECT FOR CASE
					if(Hindi_M==Hindi_F):
						G = 'U'
					HST_index= HST_index+1 #Next word in Hindi, since ADJN, always feasible because adjective will not be last word of sentence
					H_noun = HST[HST_index]
					next = HST[HST_index+1] #also feasible because can't end a sentence with 'bada kela'
					#NOW TO DECIDE THE CASE OF H_noun: H_noun will be in accusative if followed by postposition or by 'ko'
					#can be coded later
					if(next=='ko'): # in 'kutta bade kutte par baitha'
						Noun_Lexicon.update({word[0]: [Saved_Nominative_Inflection, G, H_noun]}) #save in accusative_inflectiion
						updated = True
					else:
						Noun_Lexicon.update({word[0]: [H_noun, G, Saved_Accusative_Inflection]})
						updated = True
					if(G=='F'):
						Noun_Lexicon.update({word[0]: [H_noun, G, H_noun]}) #nominative, accusative same for female nouns
						updated = True
					if(not H_noun.endswith('e') and not H_noun.endswith('a')):
						Noun_Lexicon.update({word[0]: [H_noun, G, H_noun]}) #nominative, accusative same for male nouns not ending in 'a'
						updated = True
			if(Current_word_tag=='ADP' and Current_word in ADP_Lexicon):
				Hindi_P = ADP_Lexicon[Current_word]
				#print(Hindi_P)
				HST_index = 0
				found =False
				Current_word_h = ''
				for Hindi_word in HST:
					if(Hindi_word == Hindi_P):
						Current_word_h = Hindi_word
						#print(Current_word_h)
						found = True
				if(found):
					HST_index = HST.index(Current_word_h) #what if multiple instances? Constraint: only one
					HST_index= HST_index-1 #Previous word in Hindi, since NP, always feasible because postposition will not be first word of sentence: CONSTRAINT: 'upar ke taare chamke' not allowed
					if(HST[HST_index]=='ke'): #many postpositions will do this: table ke upar, neeche, etc.
						HST_index = HST_index -1
					H_noun = HST[HST_index]
					if(H_noun.endswith('e') and H_noun != word[0]): #inflected for prepositions, only male nouns do this! ASSUMPTION: not dealing with some female noun that may end in 'e'
					#second condition, because some english nouns may stay as they are: e.g. table, and if they end in 'e' that'll be a problem
						Noun_Lexicon.update({word[0]: [Saved_Nominative_Inflection, 'M', H_noun]}) #save in accusative_inflectiion
						updated = True
					else:
						Noun_Lexicon.update({word[0]: [H_noun, Saved_Gender, H_noun]})
						updated = True

			if(Current_word_tag=='VERB' and Current_word in Verb_Lexicon):
				Hindi_M = Verb_Lexicon[Current_word][0] #male_inflection
			#	print(Hindi_M)
				Hindi_F = Verb_Lexicon[Current_word][1] #female_inflection
			#	print(Hindi_F)
				HST_index = 0
				found =False
				if(index!=EST_size-1): #if there is anything after the object- this is admissible because no adverbs
					noun_phrase_present=True 
				Current_word_h = ''
				for Hindi_word in HST:
					if(Hindi_word == Hindi_F or Hindi_word == Hindi_M):
						Current_word_h = Hindi_word
						found = True		#Since English is SVO, if we move backwards from the noun, the noun: O.	It is also possible that the verb is present in her lexicon but not the right inflection of it, in which she will not learn anything
				token = [Current_word, Current_word_tag]
				EST_index = search_index
				AD_absent=True
				while(EST[EST_index][0] != word[0]):
					if(EST[EST_index][1] == 'ADP'):
						AD_absent= False
					EST_index= EST_index+1
				if(found and AD_absent and noun_phrase_present==False): # interceding prepositions give rise to sentences like 'The cat is on the table': Gina cannot learn table from is, this is not SVO
					#print("Here")
					HST_index = HST.index(Current_word_h) #only one instance
					HST_index= HST_index-1 #Previous word in Hindi, since Hindi: SOV, always feasible because verb will not be first word of sentence
					H_noun = HST[HST_index] #object will immediately precede the verb, because confounding adjectives will come before the noun-object. There can be no confounding prepositions: 'The cat eats the rat on the table' is not allowed because it has a prepositional clause
					if(H_noun=='ko'):
						HST_index= HST_index-1 #skip ergative marker
						H_noun = HST[HST_index]
						Noun_Lexicon.update({word[0]: [Saved_Nominative_Inflection, Saved_Gender, H_noun]}) #save in accusative_inflectiion, since 'ko' has been used
					else:
						Noun_Lexicon.update({word[0]: [H_noun, Saved_Gender, Saved_Accusative_Inflection]})
						updated = True
						#'ko' not used, not marked for accusative case
					if(Saved_Gender == 'F' or (not H_noun.endswith('e') and not H_noun.endswith('a'))):
						Noun_Lexicon.update({word[0]: [H_noun, Saved_Gender, H_noun]}) #nominative, accusative same for male nouns not ending in 'a'
					#The verb inflects for subject not object, so Gina cannot figure out the gender of H_noun
						updated = True
			if(Current_word_tag=='NOUN' and Current_word in Noun_Lexicon):
				Hindi_SN = Noun_Lexicon[Current_word][0] #has to be nominative inflection: Hindi_SN: subject noun
			#	print(Hindi_M)
				HST_index = 0
				found =False
				if(index!=EST_size-1): #if there is anything after the object- this is admissible because no adverbs
					noun_phrase_present=True 
				Current_word_h = ''
				for Hindi_word in HST:
					if(Hindi_word == Hindi_SN):
						Current_word_h = Hindi_word
						found = True		#Since English is SVO, if we move backwards from the noun, the noun: O.	It is also possible that the verb is present in her lexicon but not the right inflection of it, in which she will not learn anything
				#Checking for presence of confounding adjectives attaching to object noun, which will come between S and O
				token = [Current_word, Current_word_tag]
				EST_index =search_index #only one instance
				#print(EST[EST_index][0])
				#print(word[0])
				AD_absent=True #FIX THIS
				while(EST[EST_index][0] != word[0]):
					if(EST[EST_index][1] == 'ADJ' or EST[EST_index][1] == 'ADP'):
						AD_absent= False
					EST_index= EST_index+1
				if(found and AD_absent and noun_phrase_present==False):
					HST_index = HST.index(Current_word_h) #only one instance
					HST_index= HST_index+1#Next word in Hindi, since Hindi: SOV, always feasible because subject will not be last word of sentence
					if(HST[HST_index] =='ek'): #skip article
						HST_index= HST_index+1
					H_noun = HST[HST_index] #object will immediately precede the verb, because confounding adjectives will come before the noun-object. There can be no confounding prepositions: 'The cat eats the rat on the table' is not allowed because it has a prepositional clause
					#print(HST_index)
					HST_index= HST_index+1
					if(HST[HST_index]=='ko'):
						Noun_Lexicon.update({word[0]: [Saved_Nominative_Inflection, Saved_Gender, H_noun]}) #save in accusative_inflectiion, since 'ko' has been used
						updated = True
					else:
						Noun_Lexicon.update({word[0]: [H_noun, Saved_Gender, Saved_Accusative_Inflection]})
						updated = True
						 #'ko' not used, not marked for accusative case
					if(Saved_Gender=='F' or (not H_noun.endswith('e') and not H_noun.endswith('a'))):
						Noun_Lexicon.update({word[0]: [H_noun, Saved_Gender, H_noun]}) #nominative, accusative same for male nouns not ending in 'a', all female nouns. Gender still unknown
						updated = True
					
			if(Current_word_tag=='PRON' and Current_word in Pronoun_Lexicon):
				Hindi_SN = Pronoun_Lexicon[Current_word] #has to be nominative inflection: Hindi_SN: subject noun
			#	print(Hindi_M)
				if(Current_word=='you'):
					Hindi_SN = Pronoun_Lexicon[Current_word][0] #has to be nominative inflection: Hindi_SN: subject noun
				HST_index = 0
				found =False
				if(index!=EST_size-1): #if there is anything after the object- this is admissible because no adverbs
					noun_phrase_present=True 
				Current_word_h = ''
				for Hindi_word in HST:
					if(Hindi_word == Hindi_SN):
						Current_word_h = Hindi_word
						found = True		#Since English is SVO, if we move backwards from the noun, the noun: O.	It is also possible that the verb is present in her lexicon but not the right inflection of it, in which she will not learn anything
				#Checking for presence of confounding adjectives attaching to object noun, which will come between S and O
				token = [Current_word, Current_word_tag]
				EST_index = EST.index(token) #only one instance
				#print(EST[EST_index][0])
				#print(word[0])
				AD_absent=True
				while(EST[EST_index][0] != word[0]):
					if(EST[EST_index][1] == 'ADJ' or EST[EST_index][1] == 'ADP'):
						AD_absent= False
					EST_index= EST_index+1
				if(found and AD_absent and noun_phrase_present==False):
					HST_index = HST.index(Current_word_h) #only one instance
					HST_index= HST_index+1#Next word in Hindi, since Hindi: SOV, always feasible because subject will not be last word of sentence
					if(HST[HST_index] =='ek'): #skip article
						HST_index= HST_index+1
					H_noun = HST[HST_index] #object will immediately precede the verb, because confounding adjectives will come before the noun-object. There can be no confounding prepositions: 'The cat eats the rat on the table' is not allowed because it has a prepositional clause
					HST_index= HST_index+1
					if(HST[HST_index]=='ko'):
						Noun_Lexicon.update({word[0]: [Saved_Nominative_Inflection, Saved_Gender, H_noun]})
						updated = True	 #save in accusative_inflectiion, since 'ko' has been used
					else:
						Noun_Lexicon.update({word[0]: [H_noun, Saved_Gender, Saved_Accusative_Inflection]}) #'ko' not used, not marked for accusative case
					if(not H_noun.endswith('e') and not H_noun.endswith('a')):
						Noun_Lexicon.update({word[0]: [H_noun, Saved_Gender, H_noun]}) #nominative, accusative same for male nouns not ending in 'a', all female nouns. Gender still unknown
						updated = True
			search_index=search_index-1 #decreement search_index to go leftwards
		search_index = index +1
		while(search_index < EST_size and (updated==False or (Noun_Lexicon[word[0]][0]=='' or Noun_Lexicon[word[0]][1]=='U' or Noun_Lexicon[word[0]][2]==''))): #Going rightwards:
			if(word[0] in Noun_Lexicon):
				Saved_Nominative_Inflection = Noun_Lexicon[word[0]][0]
				Saved_Gender = Noun_Lexicon[word[0]][1]
				Saved_Accusative_Inflection = Noun_Lexicon[word[0]][2]
			else:
				Saved_Nominative_Inflection=''
				Saved_Gender='U'
				Saved_Accusative_Inflection=''
				Current_word = EST[search_index][0]
			Current_word = EST[search_index][0]
			Current_word_tag = EST[search_index][1]
			noun_phrase_present=False
			if(Current_word_tag=='VERB' and Current_word in Verb_Lexicon):
				Hindi_M = Verb_Lexicon[Current_word][0] #male_inflection
			#	print(Hindi_M)
				Hindi_F = Verb_Lexicon[Current_word][1] #female_inflection
			#	print(Hindi_F)
				HST_index = 0
				found = False
				Current_word_h = ''
				for Hindi_word in HST:
					if(Hindi_word == Hindi_F or Hindi_word == Hindi_M):
						Current_word_h = Hindi_word
						found = True		#Since English is SVO, if we move forwards from the noun, the noun: S.	It is also possible that the verb is present in her lexicon but not the right inflection of it, in which she will not learn anything
				token = [Current_word, Current_word_tag]
				EST_index = search_index #only one instance
				AD_absent=True
				Obj_exists=False
				while((EST_index < EST_size) and (EST[EST_index][1] != 'NOUN' and EST[EST_index][1] != 'PRON')): #until we reach the object if it exists
					if(EST[EST_index][1] == 'ADP' or EST[EST_index][1] == 'ADJ'):
						AD_absent= False
					EST_index= EST_index+1
				if(EST_index!=EST_size):
					Obj_exists=True
					if(EST_index!=EST_size-1): #there is something after the object if it exists
						noun_phrase_present=True
				if(found and AD_absent and noun_phrase_present==False): # interceding prepositions give rise to sentences like 'The cat is on the table': Gina cannot learn table from is, this is not SVO
					HST_index = HST.index(Current_word_h) #only one instance
					if(Current_word_h == Hindi_F):
						G = 'F'
					elif(Current_word_h == Hindi_M):
						G = 'M'
					if(Obj_exists):
						HST_index= HST_index-1 #We have reached the object in Hindi SOV
						if(HST[HST_index] == 'ko'):
							HST_index= HST_index-1 #We have reached the object in Hindi SOV
					HST_index= HST_index-1  #We have reached the subject in Hindi SOV, there were no confounding adjectives
					if(HST[HST_index] =='ek'): #skip article
						HST_index= HST_index-1
					H_noun = HST[HST_index]
					Noun_Lexicon.update({word[0]: [H_noun, G, Saved_Accusative_Inflection]}) #'ko' not used, not marked for accusative case
					updated = True
					if(G=='F' or (not H_noun.endswith('e') and not H_noun.endswith('a'))):
						Noun_Lexicon.update({word[0]: [H_noun, G, H_noun]}) #nominative, accusative same for male nouns not ending in 'a'; nominative, accusative same for female nouns
						updated = True
						
			if(Current_word_tag=='NOUN' and Current_word in Noun_Lexicon):
				Hindi_ON = Noun_Lexicon[Current_word][2] #has to be accusative inflection: Hindi_ON: subject noun
			#	print(Hindi_M)
				HST_index = 0
				found =False

				Current_word_h = ''
				for Hindi_word in HST:
					if(Hindi_word == Hindi_ON):
						Current_word_h = Hindi_word
						found = True		#Since English is SVO, if we move backwards from the noun, the noun: O.	It is also possible that the verb is present in her lexicon but not the right inflection of it, in which she will not learn anything
				#Checking for presence of confounding adjectives attaching to object noun, which will come between S and O
				token = [Current_word, Current_word_tag]
				EST_index = search_index #only one instance
				if(EST_index!=EST_size-1):
					noun_phrase_present=True
				#print(EST[EST_index][0])
				#print(word[0])
				AD_absent=True
				while(EST[EST_index][0] != word[0]):
					if(EST[EST_index][1] == 'ADJ' or EST[EST_index][1] == 'ADP'):
						AD_absent= False
					EST_index= EST_index-1

				if(found and AD_absent and noun_phrase_present==False):
					#print("Here")
					HST_index = HST.index(Current_word_h) #only one instance
					HST_index= HST_index-1#Prev word in Hindi, since Hindi: SOV, always feasible because object will not be first word of sentence
					if(HST[HST_index] =='ek'): #skip article
						HST_index= HST_index-1
					H_noun = HST[HST_index] #object will immediately precede the verb, because confounding adjectives will come before the noun-object. There can be no confounding prepositions: 'The cat eats the rat on the table' is not allowed because it has a prepositional clause
					Noun_Lexicon.update({word[0]: [H_noun, Saved_Gender, Saved_Accusative_Inflection]}) #'ko' not used, not marked for accusative case
					updated = True
					if(Saved_Gender=='F' or (not H_noun.endswith('e') and not H_noun.endswith('a'))):
						Noun_Lexicon.update({word[0]: [H_noun, Saved_Gender, H_noun]}) #nominative, accusative same for male nouns not ending in 'a', all female nouns. Gender still unknown
						updated = True
			if(Current_word_tag=='PRON' and Current_word in Pronoun_Lexicon): #pronouns in accusative inflection
				Hindi_ON = Pronoun_Lexicon[Current_word] #has to be accusative inflection: Hindi_ON: subject noun
			#	print(Hindi_M)
				if(Current_word=='you'):
					Hindi_ON = Pronoun_Lexicon[Current_word][1] #has to be accusative inflection: Hindi_SN: subject noun
				HST_index = 0
				found =False
				Current_word_h = ''
				for Hindi_word in HST:
					if(Hindi_word == Hindi_ON):
						Current_word_h = Hindi_word
						found = True		#Since English is SVO, if we move backwards from the noun, the noun: O.	It is also possible that the verb is present in her lexicon but not the right inflection of it, in which she will not learn anything
				#Checking for presence of confounding adjectives attaching to object noun, which will come between S and O
				token = [Current_word, Current_word_tag]
				EST_index = EST.index(token) #only one instance
				if(EST_index!=EST_size-1):
					noun_phrase_present=True
				#print(EST[EST_index][0])
				#print(word[0])
				AD_absent=True
				while(EST[EST_index][0] != word[0]):
					if(EST[EST_index][1] == 'ADJ' or EST[EST_index][1] == 'ADP'):
						AD_absent= False
					EST_index= EST_index-1
				if(found and AD_absent and noun_phrase_present==False):
					HST_index = HST.index(Current_word_h)
					HST_index= HST_index - 1 #Previous word in Hindi, since Hindi: SOV, always feasible because subject will not be last word of sentence
					if(HST[HST_index] =='ek'): #skip article
						HST_index= HST_index-1
						H_noun = HST[HST_index] #object will immediately precede the verb, because confounding adjectives will come before the noun-object. There can be no confounding prepositions: 'The cat eats the rat on the table' is not allowed because it has a prepositional clause
					Noun_Lexicon.update({word[0]: [H_noun, Saved_Gender, Saved_Accusative_Inflection]}) #'ko' not used, not marked for accusative case
					updated = True
					if(Saved_Gender=='F' or (not H_noun.endswith('e') and not H_noun.endswith('a'))):
						Noun_Lexicon.update({word[0]: [H_noun, Saved_Gender, H_noun]}) #nominative, accusative same for male nouns not ending in 'a', all female nouns. Gender still unknown
						updated = True
			search_index=search_index+1 #decreement search_index to go leftwards
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
