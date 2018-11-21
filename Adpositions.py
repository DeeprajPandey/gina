import json
#PREPOSITIONS
#MAJOR ASSUMPTION: USER WILL ENTER THE ENTIRE PREPOSITION JAMMED INTO ONE WORD
#Function has: EST, HST. Access to all lexicons.
#EST = [[token, tag]]
#HST = [token]
#NOUNLEXICON: Englishkey : [nominative_inflection, grammatical_gender, accusative_inflection]
Noun_Lexicon = {'cat': ['billi', 'F', 'billi']} #G: M, F, U.
#VERBLEXICON: Englishkey : [male_inflection, female_inflection, person] Person: if the English is in 'First Person' or 'Third Person'
Verb_Lexicon = { 'eats': ['khata', 'khaati', 'Third Person']}
#ADJECTIVELEXICON: Englishkey :  [male_inflection, female_inflection, accusative_inflection]
ADJ_Lexicon = {'big': ['bada', 'badi', 'bade'], 'small': ['chhota', 'chhoti', '']}
#ADPOSITIONLEXICON: Englishkey : postposition
ADP_Lexicon = {'in': 'mein'}
#PRONOUNLEXICON: Englishkey: [nominative_inflection, accusative_inflection]
Pronoun_Lexicon = {'I': 'main', 'me': 'mujhko', 'you': ['tu', 'tujhko'], 'he': 'voh', 'him': 'usko', 'she': 'voh', 'her': 'usko'} #Print this and provide spelling to user
#EST = [['The', 'DET'], ['rat', 'NOUN'],['eats', 'VERB'], ['on', 'ADP'] , ['the', 'DET'], ['cat', 'NOUN']]
with open('JSON/partsOfSpeech.json', 'r') as f: #calling partsOfSpeech.json for read and storing it into a dictionary
    pos_dict = json.loads(f.read())

for x in pos_dict["tokens"]:
    row = []
    if x["partOfSpeech"]["tag"] == "PUNCT":#not storing punctuation marks in EST
        continue #if a "PUNCT" is encountered, then the nothing is appended and
    row.append(x["text"]["content"])
    row.append(x["partOfSpeech"]["tag"])
    EST.append(row)
HST = ['chuha', 'billi', 'par', 'khata', 'hai']
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
					Hindi_ADP = HST[HST_index]
					ADP_Lexicon.update({word[0]: Hindi_ADP})
					updated = True
			search_index = search_index+1
print(ADP_Lexicon)
