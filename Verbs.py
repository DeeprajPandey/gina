import json
#VERBS
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

#EST = [['The', 'DET'], ['you', 'PRON'],['write', 'VERB'], ['on', 'ADP'], ['the', 'DET'], ['me', 'PRON']]
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
HST = ['tun', 'mujh', 'par', 'likhta', 'hai']
HST_size = len(HST)
EST_size = len(EST)
index=-1;
for word in EST:
	index=index+1 #gives us the index of word
	if(word[1]=='VERB' and word[0] not in Verb_Lexicon): #UNKNOWN VERB
		G ='' #grammatical gender
		search_index = index -1
		updated = False
		while(search_index > -1 and updated==False):
			Current_word = EST[search_index][0]
			#print(Current_word)
			Current_word_tag = EST[search_index][1]
			if(Current_word_tag=='NOUN' and Current_word in Noun_Lexicon):
				Hindi_N = Noun_Lexicon[Current_word][0] #always in nominative form as the noun is the subject of the sentence
				NG= Noun_Lexicon[Current_word][1] #to learn gender of verb
				HST_index = 0
				found = False
				Current_word_h = ''
				for Hindi_word in HST:
					if(Hindi_word == Hindi_N):
						Current_word_h = Hindi_word
						found = True		#Since English is SVO, if we move backwards from the noun, the noun: O.	It is also possible that the verb is present in her lexicon but not the right inflection of it, in which she will not learn anything
				token = [Current_word, Current_word_tag] #the subject
				EST_index = EST.index(token) + 1  #only one instance, starting from next
				ADP_count=0
				Obj_exists=False
				while((EST_index < EST_size) and (EST[EST_index][1] != 'NOUN' and EST[EST_index][1] != 'PRON')): #until we reach the object if it exists
					if(EST[EST_index][1] == 'ADP' or EST[EST_index][1] == 'ADJ'):
						ADP_count= ADP_count+1
					EST_index= EST_index+1
				print(EST_index)
				if(EST_index!=EST_size):
					Obj_exists=True
				#print('ADP: ', ADP_count)
				#print(Obj_exists)
				if(found): # interceding prepositions give rise to sentences like 'The cat is on the table'
					HST_index = HST.index(Current_word_h) #only one instance
					VG = NG #verb inflects for subject
					HST_index= HST_index+1 #We have reached the verb in Hindi SOV if object doesn't exist: SV
					if(Obj_exists):
						HST_index= HST_index+1 + ADP_count #We have reached the object in Hindi SOV
						if(HST[HST_index] == 'ko'):
							HST_index= HST_index+1
					H_verb = HST[HST_index]
					Person = 'Third Person' #because there were no plural nouns, and the subject was a noun, not the pronoun 'I'
					if(VG=='U'):
						if(H_verb.endswith('a')):
							VG='M'
						elif(H_verb.endswith('i') or H_verb.endswith('ee')):
							VG ='F'
					if(VG=='M'):
						if(word[0] in Verb_Lexicon):
							H_verb_F = Verb_Lexicon[word[0]][1]
						else:
							H_verb_F = ''
						Verb_Lexicon.update({word[0]: [H_verb, H_verb_F, Person]})
						updated = True
					if(VG=='F'):
						if(word[0] in Verb_Lexicon):
							H_verb_M = Verb_Lexicon[word[0]][0]
						else:
							H_verb_M = ''
						Verb_Lexicon.update({word[0]: [H_verb_M, H_verb, Person]})
						updated = True
			if(Current_word_tag=='PRON' and Current_word in Pronoun_Lexicon):
				Hindi_Pro = Pronoun_Lexicon[Current_word] #always in nominative form as the noun is the subject of the sentence
				if(Current_word=='you'):
					Hindi_Pro = Pronoun_Lexicon[Current_word][0] #since it is the subject, it will be in the nominative: i.e. 'tu'
				HST_index = 0
				found = False
				Current_word_h = ''
				for Hindi_word in HST:
					if(Hindi_word == Hindi_Pro):
						Current_word_h = Hindi_word
						found = True		#necessary to double check if the user has entered the 'right' Hindi pronoun, not 'aap' for 'you' etc.
				token = [Current_word, Current_word_tag] #the subject
				EST_index = EST.index(token) + 1  #only one instance, starting from next token
				ADJ_count=0
				ADP_count=0
				Obj_exists=False
				while((EST_index < EST_size) and (EST[EST_index][1] != 'NOUN' and EST[EST_index][1] != 'PRON')): #until we reach the object if it exists
					if(EST[EST_index][1] == 'ADP'):
						ADP_count= ADP_count+1
					if(EST[EST_index][1] == 'ADJ'):
						ADJ_count=ADJ_count+1
					EST_index= EST_index+1
				#print(EST_index)
				if(EST_index!=EST_size): #if it has iterated through the whole list, object was not encountered
					Obj_exists=True
				#print(Obj_exists)
				#print(found)
				if(found): # interceding prepositions give rise to sentences like 'The cat is on the table'
					HST_index = HST.index(Current_word_h) #only one instance
					HST_index= HST_index+1 #We have reached the verb in Hindi SOV if object doesn't exist: SV, since there are no adverbs. Else we've reached object
					if(Obj_exists):
						HST_index= HST_index+1 + ADP_count + ADJ_count #We have reached the object in Hindi SOV, ADP, ADJ will only exist if object exists, since they attach to object
						if(HST[HST_index] == 'ko'):
							HST_index= HST_index+1
					H_verb = HST[HST_index]
					if(Current_word=='you' or Current_word=='I'):
						Person = 'First, Second Person' #First, Second person is identical is English: e.g. I eat, you eat.
					else:
						Person = 'Third Person' #because there were no plural nouns, and the subject was a noun, not the pronoun 'I'
					if(H_verb.endswith('a')): #ASSUMPTION: generally tends to be true in Hindi
						VG='M'
					elif(H_verb.endswith('i') or H_verb.endswith('ee')):
						VG ='F'
					else:
						VG = 'U'
					if(VG=='M'):
						if(word[0] in Verb_Lexicon):
							H_verb_F = Verb_Lexicon[word[0]][1]
						else:
							H_verb_F = ''
						Verb_Lexicon.update({word[0]: [H_verb, H_verb_F, Person]})
						updated = True
					if(VG=='F'):
						if(word[0] in Verb_Lexicon):
							H_verb_M = Verb_Lexicon[word[0]][0]
						else:
							H_verb_M = ''
						Verb_Lexicon.update({word[0]: [H_verb_M, H_verb, Person]})
						updated = True
			search_index = search_index -1
		search_index = index + 1 # token after verb
		print(search_index)
		while(search_index < EST_size and updated==False):
			Current_word = EST[search_index][0]
			print(Current_word)
			Current_word_tag = EST[search_index][1]
			if(Current_word_tag=='NOUN' and Current_word in Noun_Lexicon):
				#print(1)
				Hindi_N = Noun_Lexicon[Current_word][2] #always in accusative form as the noun is the object of the sentence
				#print(Hindi_N)
				HST_index = 0
				found = False
				Current_word_h = ''
				for Hindi_word in HST:
					#print(Hindi_word)
					if(Hindi_word == Hindi_N):
						Current_word_h = Hindi_word
						found = True	#neccessary, because although the noun is present, its accusative inflection might not be
				print(found)
				token = [Current_word, Current_word_tag] #the subject
				EST_index = EST.index(token) -1  #only one instance, starting from previous to check for existence of preposition
				ADP_count=0
				print(EST_index)
				while(EST[EST_index][0] != word[0]): #until we reach the verb
					if(EST[EST_index][1] == 'ADP'):
						ADP_count= ADP_count+1
					EST_index= EST_index-1
				print(EST_index)
				print(ADP_count)
				if(found):
					HST_index = HST.index(Current_word_h) #only one instance
					print(HST_index)
					HST_index= HST_index+1+ ADP_count #We have reached the verb in Hindi: SOV, if there is no 'ko', whether or not there were adjectives, because these would come before the object; we have added 1 if presence of preposition
					print('HST_index', HST_index)
					if(HST[HST_index] == 'ko'):
						HST_index= HST_index+1 #skip the 'ko' to reach verb
					H_verb = HST[HST_index]
					print(H_verb)
					Person =''
					if(word[0].endswith('s')): #most third person English verbs end in 's'
						Person = 'Third Person' #because there were no plural nouns, and had the subject been 'I' or 'you', we would have located it in above module; the above if statement is just to double-check
					if(H_verb.endswith('a')): #generalisation
						VG='M'
					elif(H_verb.endswith('i') or H_verb.endswith('ee')): #generalisation
						VG ='F'
					if(VG=='M' and Person != ''):
						if(word[0] in Verb_Lexicon):
							H_verb_F = Verb_Lexicon[word[0]][1]
						else:
							H_verb_F = ''
						Verb_Lexicon.update({word[0]: [H_verb, H_verb_F, Person]})
						updated = True
					if(VG=='F' and Person != ''):
						if(word[0] in Verb_Lexicon):
							H_verb_M = Verb_Lexicon[word[0]][0]
						else:
							H_verb_M = ''
						Verb_Lexicon.update({word[0]: [H_verb_M, H_verb, Person]})
						updated= True
			if(Current_word_tag=='PRON' and Current_word in Pronoun_Lexicon):
				#print(1)
				Hindi_N = Pronoun_Lexicon[Current_word] #always in accusative form as the noun is the object of the sentence
				Hindi_Pro = Pronoun_Lexicon[Current_word] #always in nominative form as the noun is the subject of the sentence
				if(Current_word=='you'):
					Hindi_Pro = Pronoun_Lexicon[Current_word][1] #since it is the subject, it will be in the nominative: i.e. 'tu'
				#print(Hindi_N)
				HST_index = 0
				found = False
				Current_word_h = ''
				for Hindi_word in HST:
					#print(Hindi_word)
					if(Hindi_word == Hindi_N):
						Current_word_h = Hindi_word
						found = True	#neccessary, because although the noun is present, its accusative inflection might not be
				print(found)
				token = [Current_word, Current_word_tag] #the subject
				EST_index = EST.index(token) -1  #only one instance, starting from previous to check for existence of preposition
				ADP_count=0
				print(EST_index)
				while(EST[EST_index][0] != word[0]): #until we reach the verb
					if(EST[EST_index][1] == 'ADP'):
						ADP_count= ADP_count+1
					EST_index= EST_index-1
				print(EST_index)
				print(ADP_count)
				if(found):
					HST_index = HST.index(Current_word_h) #only one instance
					print(HST_index)
					HST_index= HST_index+1+ ADP_count #We have reached the verb in Hindi: SOV, if there is no 'ko', whether or not there were adjectives, because these would come before the object; we have added 1 if presence of preposition
					print('HST_index', HST_index)
					if(HST[HST_index] == 'ko'):
						HST_index= HST_index+1 #skip the 'ko' to reach verb
					H_verb = HST[HST_index]
					print(H_verb)
					Person =''
					if(word[0].endswith('s')): #most third person English verbs end in 's'
						Person = 'Third Person'#because there were no plural nouns
					else:
						Person =  'First, Second Person' #no plural pronouns
					if(H_verb.endswith('a')): #generalisation
						VG='M'
					elif(H_verb.endswith('i') or H_verb.endswith('ee')): #generalisation
						VG ='F'
					if(VG=='M' and Person != ''):
						if(word[0] in Verb_Lexicon):
							H_verb_F = Verb_Lexicon[word[0]][1]
						else:
							H_verb_F = ''
						Verb_Lexicon.update({word[0]: [H_verb, H_verb_F, Person]})
						updated = True
					if(VG=='F' and Person != ''):
						if(word[0] in Verb_Lexicon):
							H_verb_M = Verb_Lexicon[word[0]][0]
						else:
							H_verb_M = ''
						Verb_Lexicon.update({word[0]: [H_verb_M, H_verb, Person]})
						updated= True
			search_index = search_index +1
# Load the updated lexicon to the file
updated_lex = {
    "nouns": Noun_Lexicon,
    "verbs": Verb_Lexicon,
    "adjectives": ADJ_Lexicon,
    "adpositions": ADP_Lexicon,
    "pronouns": Pronoun_Lexicon
}
with open('JSON/lexicon.json', 'w') as fp:
    json.dump(updated_lex, fp)
